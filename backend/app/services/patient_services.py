"""
Patient Management Service

This module provides the core functionality for managing patients in the dental clinic system.
It handles patient registration, search, and profile management.
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.patients import Patient
from models.users import User

class PatientManagement:
    """Handles all patient-related operations in the dental clinic system."""
    
    @staticmethod
    def register_patient(
        db: Session,
        user_id: int,
        medical_history: str = "",
        allergies: str = "",
        emergency_contact: str = "",
    ) -> Patient:
        """
        Register a new patient in the system.
        
        Args:
            db: Database session
            user_id: ID of the user account associated with the patient
            medical_history: Patient's medical history
            allergies: Patient's allergies
            emergency_contact: Emergency contact information
        
        Returns:
            Newly created Patient object
        """
        patient = Patient(
            user_id=user_id,
            medical_history=medical_history,
            allergies=allergies,
            emergency_contact=emergency_contact,
            under_treatment=False
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def search_patients(
        db: Session,
        search_term: str,
        page: int = 1,
        per_page: int = 20
    ) -> List[Patient]:
        """
        Search for patients using various criteria.
        
        Args:
            db: Database session
            search_term: Search string to match against patient records
            page: Page number for pagination
            per_page: Number of results per page
        
        Returns:
            List of matching Patient objects
        """
        query = db.query(Patient).join(User).filter(
            or_(
                User.full_name.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%"),
                User.phone_number.ilike(f"%{search_term}%")
            )
        )
        return query.offset((page - 1) * per_page).limit(per_page).all()