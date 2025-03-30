from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Bug(Base):
    __tablename__ = "bug"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    classify = Column(String(16))
    module = Column(String(11))
    description = Column(Text)
    status = Column(String(20), default="open")
    severity = Column(String(8))
    solution = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
