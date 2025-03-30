from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import Bug, ResponseModel, BugUpdate
import uvicorn
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bugs/", status_code=201)
def create_bug(bug: Bug, db: Session = Depends(get_db)):
    new_bug = models.Bug(**bug.model_dump())
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug


@app.get("/bugs/", response_model=List[Bug])
def get_all_bugs(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    bugs = db.query(models.Bug).offset(skip).limit(limit).all()
    return bugs


@app.delete("/bugs/{bug_id}")
def delete_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if bug is None:
        raise HTTPException(status_code=404, detail="Bug not found")

    db.delete(bug)
    db.commit()
    return {"message": "Bug deleted successfully"}


@app.put("/bugs/{bug_id}", response_model=Bug)
def update_bug(bug_id: int, bug: BugUpdate, db: Session = Depends(get_db)):
    db_bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if db_bug is None:
        raise HTTPException(status_code=404, detail="Bug not found")

    update_data = bug.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bug, field, value)

    db.commit()
    db.refresh(db_bug)
    return db_bug


@app.get("/bugs/{bug_id}", response_model=Bug)
def get_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if bug is None:
        raise HTTPException(status_code=404, detail="Bug not found")
    return bug


@app.get("/bugs/search/", response_model=List[Bug])
def search_bugs(
        query: str = Query(..., description="Search in title and description"),
        db: Session = Depends(get_db)
):
    bugs = db.query(models.Bug).filter(
        (models.Bug.title.contains(query)) |
        (models.Bug.description.contains(query))
    ).all()
    return bugs


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)


