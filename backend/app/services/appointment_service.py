"""
Appointment Management Service

This module provides the core functionality for managing dental appointments.
It handles scheduling, conflict detection, and appointment status management.
The service ensures proper coordination between patients, dentists, and treatments.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.appointments import Appointment, AppointmentStatus
from models.treatments import Treatment
from models.dentists import Dentist

class AppointmentSystem:
    """
    Manages dental appointments and scheduling.
    
    This class provides methods for creating, managing, and tracking dental appointments.
    It includes sophisticated conflict detection to prevent double-booking and ensures
    that appointments are properly scheduled considering treatment durations.
    """
    
    @staticmethod
    def schedule_appointment(
        db: Session,
        patient_id: int,
        dentist_id: int,
        treatment_id: int,
        datetime: datetime,
        notes: str = "",
        created_by_id: Optional[int] = None
    ) -> Appointment:
        """
        Schedule a new appointment with conflict checking.
        
        This method creates a new appointment after verifying that the time slot
        is available for the specified dentist. It considers the duration of the
        requested treatment when checking for conflicts.
        
        Args:
            db: Database session for performing operations
            patient_id: ID of the patient receiving treatment
            dentist_id: ID of the dentist performing treatment
            treatment_id: ID of the scheduled treatment
            datetime: Date and time of the appointment
            notes: Optional notes about the appointment
            created_by_id: Optional ID of user creating the appointment
        
        Returns:
            Newly created Appointment object
        
        Raises:
            ValueError: If the time slot is not available or if any referenced
                       entities (patient, dentist, treatment) don't exist
        """
        # Check for scheduling conflicts
        if AppointmentSystem.has_conflict(db, dentist_id, datetime, treatment_id):
            raise ValueError("Time slot is not available for the specified dentist")

        appointment = Appointment(
            patient_id=patient_id,
            dentist_id=dentist_id,
            treatment_id=treatment_id,
            datetime=datetime,
            notes=notes,
            status=AppointmentStatus.SCHEDULED,
            created_by_id=created_by_id
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def has_conflict(
        db: Session,
        dentist_id: int,
        datetime: datetime,
        treatment_id: int
    ) -> bool:
        """
        Check for scheduling conflicts with existing appointments.
        
        This method performs a detailed check to ensure that the proposed appointment
        time doesn't overlap with any existing appointments, considering the duration
        of both the proposed and existing treatments.
        
        Args:
            db: Database session
            dentist_id: ID of the dentist to check
            datetime: Proposed appointment time
            treatment_id: ID of the treatment to be scheduled
        
        Returns:
            True if there is a conflict, False if the time slot is available
        """
        treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
        if not treatment:
            raise ValueError("Treatment not found")
        
        end_time = datetime + timedelta(minutes=treatment.duration_minutes)
        
        existing = db.query(Appointment).filter(
            and_(
                Appointment.dentist_id == dentist_id,
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED,
                    AppointmentStatus.CONFIRMED
                ]),
                or_(
                    # Check if new appointment starts during an existing one
                    and_(
                        Appointment.datetime >= datetime,
                        Appointment.datetime < end_time
                    ),
                    # Check if existing appointment overlaps with new one
                    and_(
                        Appointment.datetime <= datetime,
                        Appointment.datetime + timedelta(minutes=treatment.duration_minutes) > datetime
                    )
                )
            )
        ).first()
        
        return existing is not None

    @staticmethod
    def update_appointment_status(
        db: Session,
        appointment_id: int,
        new_status: AppointmentStatus,
        notes: Optional[str] = None
    ) -> Appointment:
        """
        Update the status of an existing appointment.
        
        This method allows tracking the lifecycle of appointments from scheduled
        through completed or cancelled states.
        
        Args:
            db: Database session
            appointment_id: ID of the appointment to update
            new_status: New status to set
            notes: Optional notes about the status change
        
        Returns:
            Updated Appointment object
        """
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if not appointment:
            raise ValueError("Appointment not found")
        
        appointment.status = new_status
        if notes:
            appointment.notes = (appointment.notes or "") + f"\n[{datetime.now()}] {notes}"
        
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def get_dentist_schedule(
        db: Session,
        dentist_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Appointment]:
        """
        Retrieve a dentist's schedule for a specific date range.
        
        This method returns all appointments for a dentist within the specified
        time period, useful for schedule management and planning.
        
        Args:
            db: Database session
            dentist_id: ID of the dentist
            start_date: Start of the date range
            end_date: End of the date range
        
        Returns:
            List of appointments within the specified date range
        """
        return db.query(Appointment).filter(
            and_(
                Appointment.dentist_id == dentist_id,
                Appointment.datetime >= start_date,
                Appointment.datetime <= end_date,
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED,
                    AppointmentStatus.CONFIRMED
                ])
            )
        ).order_by(Appointment.datetime).all()