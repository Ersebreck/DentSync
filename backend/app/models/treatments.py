# app/models/treatments.py
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from .base import Base, TimeStampMixin

class Treatment(Base, TimeStampMixin):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String)

    # Relationships
    appointments = relationship("Appointment", back_populates="treatment")
    patients = relationship("Patient", secondary="patient_treatments", back_populates="treatments")