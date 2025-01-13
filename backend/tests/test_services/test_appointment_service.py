"""
Tests for the appointment management service.
"""

import pytest
from datetime import datetime, timedelta
from app.services.appointment_service import AppointmentSystem
from app.models.appointments import AppointmentStatus

def test_schedule_appointment(db_session, sample_patient, sample_dentist, sample_treatment):
    """Test creating a new appointment."""
    appointment_time = datetime.now() + timedelta(days=1)
    
    appointment = AppointmentSystem.schedule_appointment(
        db=db_session,
        patient_id=sample_patient.id,
        dentist_id=sample_dentist.id,
        treatment_id=sample_treatment.id,
        datetime=appointment_time,
        notes="Test appointment"
    )
    
    assert appointment.patient_id == sample_patient.id
    assert appointment.dentist_id == sample_dentist.id
    assert appointment.treatment_id == sample_treatment.id
    assert appointment.status == AppointmentStatus.SCHEDULED

def test_appointment_conflict_detection(db_session, sample_patient, sample_dentist, sample_treatment):
    """Test that overlapping appointments are detected."""
    appointment_time = datetime.now() + timedelta(days=1)
    
    # Create first appointment
    AppointmentSystem.schedule_appointment(
        db=db_session,
        patient_id=sample_patient.id,
        dentist_id=sample_dentist.id,
        treatment_id=sample_treatment.id,
        datetime=appointment_time,
        notes="First appointment"
    )
    
    # Try to create overlapping appointment
    with pytest.raises(ValueError, match="Time slot is not available"):
        AppointmentSystem.schedule_appointment(
            db=db_session,
            patient_id=sample_patient.id,
            dentist_id=sample_dentist.id,
            treatment_id=sample_treatment.id,
            datetime=appointment_time + timedelta(minutes=15),
            notes="Overlapping appointment"
        )

def test_update_appointment_status(db_session, sample_patient, sample_dentist, sample_treatment):
    """Test updating appointment status."""
    appointment_time = datetime.now() + timedelta(days=1)
    
    appointment = AppointmentSystem.schedule_appointment(
        db=db_session,
        patient_id=sample_patient.id,
        dentist_id=sample_dentist.id,
        treatment_id=sample_treatment.id,
        datetime=appointment_time
    )
    
    updated_appointment = AppointmentSystem.update_appointment_status(
        db=db_session,
        appointment_id=appointment.id,
        new_status=AppointmentStatus.CONFIRMED,
        notes="Confirmed by patient"
    )
    
    assert updated_appointment.status == AppointmentStatus.CONFIRMED
    assert "Confirmed by patient" in updated_appointment.notes

def test_get_dentist_schedule(db_session, sample_patient, sample_dentist, sample_treatment):
    """Test retrieving a dentist's schedule."""
    base_time = datetime.now() + timedelta(days=1)
    
    # Create multiple appointments
    appointments = []
    for i in range(3):
        appointment = AppointmentSystem.schedule_appointment(
            db=db_session,
            patient_id=sample_patient.id,
            dentist_id=sample_dentist.id,
            treatment_id=sample_treatment.id,
            datetime=base_time + timedelta(hours=i*2)
        )
        appointments.append(appointment)
    
    # Get schedule for the day
    schedule = AppointmentSystem.get_dentist_schedule(
        db=db_session,
        dentist_id=sample_dentist.id,
        start_date=base_time.replace(hour=0, minute=0),
        end_date=base_time.replace(hour=23, minute=59)
    )
    
    assert len(schedule) == 3
    assert all(appt.id in [a.id for a in appointments] for appt in schedule)