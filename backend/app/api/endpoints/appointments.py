"""
Appointment management API endpoints.
These routes handle all appointment-related operations in the dental clinic system.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.dependencies import get_db, get_current_user
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)
from app.services.appointment_service import AppointmentSystem
from app.models.appointments import AppointmentStatus

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new appointment."""
    try:
        return AppointmentSystem.schedule_appointment(
            db=db,
            patient_id=appointment.patient_id,
            dentist_id=appointment.dentist_id,
            treatment_id=appointment.treatment_id,
            datetime=appointment.datetime,
            notes=appointment.notes,
            created_by_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Get appointment details by ID."""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Update the status of an appointment."""
    try:
        return AppointmentSystem.update_appointment_status(
            db=db,
            appointment_id=appointment_id,
            new_status=status
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/dentist/{dentist_id}/schedule", response_model=List[AppointmentResponse])
def get_dentist_schedule(
    dentist_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    _current_user = Depends(get_current_user)
):
    """Get a dentist's schedule for a specific date range."""
    return AppointmentSystem.get_dentist_schedule(
        db=db,
        dentist_id=dentist_id,
        start_date=start_date,
        end_date=end_date
    )