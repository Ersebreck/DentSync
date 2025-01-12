# app/models/staff.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimeStampMixin

class Staff(Base, TimeStampMixin):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    position = Column(String, nullable=False)
    hire_date = Column(DateTime, nullable=False)
    is_current = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="staff_profile")