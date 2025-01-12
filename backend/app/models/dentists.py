# app/models/dentists.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimeStampMixin

class Dentist(Base, TimeStampMixin):
    __tablename__ = "dentists"

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), unique=True)
    specialization = Column(String)
    license_number = Column(String, unique=True)

    # Relationships
    appointments = relationship("Appointment", back_populates="dentist")
    schedules = relationship("DentistSchedule", back_populates="dentist")
    staff = relationship("Staff")