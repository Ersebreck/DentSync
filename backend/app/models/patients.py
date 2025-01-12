# app/models/patients.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from .base import Base, TimeStampMixin

# Association table for Patient-Treatment relationship
patient_treatments = Table(
    'patient_treatments',
    Base.metadata,
    Column('patient_id', Integer, ForeignKey('patients.id'), primary_key=True),
    Column('treatment_id', Integer, ForeignKey('treatments.id'), primary_key=True)
)

class Patient(Base, TimeStampMixin):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    medical_history = Column(Text)
    allergies = Column(Text)
    under_treatment = Column(Boolean, default=False)
    notes = Column(Text)
    emergency_contact = Column(String)

    # Relationships
    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    treatments = relationship("Treatment", secondary=patient_treatments, back_populates="patients")