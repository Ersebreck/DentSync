"""
Treatment Management Service

This module provides functionality for managing dental treatments, including
creation, categorization, and tracking of treatment history. It supports the
core business operations related to dental procedures and services.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.treatments import Treatment
from models.appointments import Appointment, AppointmentStatus
from models.dentists import Dentist

class TreatmentManagement:
    """
    Handles dental treatment-related operations.
    
    This class manages the catalog of available treatments and tracks treatment
    history for patients. It provides methods for creating new treatment types
    and analyzing treatment patterns.
    """
    
    @staticmethod
    def create_treatment(
        db: Session,
        name: str,
        description: str,
        duration_minutes: int,
        price: float,
        category: Optional[str] = None
    ) -> Treatment:
        """
        Create a new treatment type in the system.
        
        This method adds a new type of dental treatment to the catalog,
        specifying its characteristics such as duration and price.
        
        Args:
            db: Database session
            name: Name of the treatment
            description: Detailed description of the treatment
            duration_minutes: Expected duration in minutes
            price: Cost of the treatment
            category: Optional category for grouping treatments
        
        Returns:
            Newly created Treatment object
        """
        # Validate duration and price
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive")
        if price < 0:
            raise ValueError("Price cannot be negative")

        treatment = Treatment(
            name=name,
            description=description,
            duration_minutes=duration_minutes,
            price=price,
            category=category
        )
        db.add(treatment)
        db.commit()
        db.refresh(treatment)
        return treatment

    @staticmethod
    def get_patient_treatment_history(
        db: Session,
        patient_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve treatment history for a specific patient.
        
        This method compiles a comprehensive history of all completed treatments
        for a patient, including details about the treatment, dentist, and date.
        
        Args:
            db: Database session
            patient_id: ID of the patient
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
        
        Returns:
            List of dictionaries containing treatment history details
        """
        query = db.query(
            Appointment,
            Treatment,
            Dentist
        ).join(
            Treatment,
            Appointment.treatment_id == Treatment.id
        ).join(
            Dentist,
            Appointment.dentist_id == Dentist.id
        ).filter(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.status == AppointmentStatus.COMPLETED
            )
        )

        if start_date:
            query = query.filter(Appointment.datetime >= start_date)
        if end_date:
            query = query.filter(Appointment.datetime <= end_date)

        results = query.order_by(Appointment.datetime.desc()).all()
        
        return [{
            'appointment_date': appt.datetime,
            'treatment_name': treatment.name,
            'treatment_category': treatment.category,
            'dentist_id': dentist.id,
            'notes': appt.notes,
            'price': treatment.price
        } for appt, treatment, dentist in results]

    @staticmethod
    def get_treatments_by_category(
        db: Session,
        category: Optional[str] = None
    ) -> List[Treatment]:
        """
        Retrieve treatments filtered by category.
        
        This method returns all treatments in a specific category, or all
        treatments if no category is specified.
        
        Args:
            db: Database session
            category: Optional category to filter by
        
        Returns:
            List of Treatment objects
        """
        query = db.query(Treatment)
        if category:
            query = query.filter(Treatment.category == category)
        return query.order_by(Treatment.name).all()

    @staticmethod
    def calculate_treatment_statistics(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Calculate statistics about treatments performed.
        
        This method generates insights about treatment patterns, including
        popular treatments, average durations, and revenue statistics.
        
        Args:
            db: Database session
            start_date: Start of the analysis period
            end_date: End of the analysis period
        
        Returns:
            Dictionary containing various treatment statistics
        """
        completed_treatments = db.query(
            Treatment,
            func.count(Appointment.id).label('count'),
            func.sum(Treatment.price).label('revenue')
        ).join(
            Appointment
        ).filter(
            and_(
                Appointment.status == AppointmentStatus.COMPLETED,
                Appointment.datetime >= start_date,
                Appointment.datetime <= end_date
            )
        ).group_by(Treatment.id).all()

        return {
            'total_treatments': sum(t[1] for t in completed_treatments),
            'total_revenue': sum(t[2] for t in completed_treatments),
            'treatment_counts': {
                t[0].name: {'count': t[1], 'revenue': t[2]}
                for t in completed_treatments
            }
        }