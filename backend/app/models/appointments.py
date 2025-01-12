# app/models/appointments.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text, Enum
from sqlalchemy.orm import relationship
import enum
from .base import Base, TimeStampMixin

class AppointmentStatus(enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class Appointment(Base, TimeStampMixin):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    notes = Column(Text)
    
    # Foreign Keys
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    treatment_id = Column(Integer, ForeignKey("treatments.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))  # User who created the appointment

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    dentist = relationship("Dentist", back_populates="appointments")
    treatment = relationship("Treatment", back_populates="appointments")
    created_by = relationship("User")