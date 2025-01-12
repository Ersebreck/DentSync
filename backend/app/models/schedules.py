# app/models/schedules.py
from sqlalchemy import Column, Integer, Time, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimeStampMixin

class DentistSchedule(Base, TimeStampMixin):
    __tablename__ = "dentist_schedules"

    id = Column(Integer, primary_key=True)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship
    dentist = relationship("Dentist", back_populates="schedules")