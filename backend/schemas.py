from pydantic import BaseModel
from typing import Optional


class Bug(BaseModel):
    title: str

    module: str
    description: str
    solution: Optional[str] = None
    status: str = None
    severity: str = None


class ResponseModel(BaseModel):
    success: bool
    data: Bug


class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None

