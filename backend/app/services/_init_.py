"""
Dental Clinic Management System - Service Layer

This package contains the business logic for the dental clinic management system.
Each module provides a service class that handles specific domain operations.
"""

from .patient_service import PatientManagement
from .appointment_service import AppointmentSystem
from .treatment_service import TreatmentManagement

__all__ = [
    'PatientManagement',
    'AppointmentSystem',
    'TreatmentManagement'
]