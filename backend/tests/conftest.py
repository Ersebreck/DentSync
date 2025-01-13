"""
Test configuration and shared fixtures for the dental clinic system tests.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.db.base import Base
from app.models.users import User, Role
from app.models.patients import Patient
from app.models.dentists import Dentist
from app.models.treatments import Treatment
from app.models.appointments import Appointment, AppointmentStatus

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="dummy_hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def sample_dentist(db_session, sample_user):
    """Create a sample dentist for testing."""
    dentist = Dentist(
        staff_id=1,
        specialization="General Dentistry",
        license_number="DEN123"
    )
    db_session.add(dentist)
    db_session.commit()
    return dentist

@pytest.fixture
def sample_treatment(db_session):
    """Create a sample treatment for testing."""
    treatment = Treatment(
        name="Regular Checkup",
        description="Standard dental examination",
        duration_minutes=30,
        price=50.00,
        category="Examination"
    )
    db_session.add(treatment)
    db_session.commit()
    return treatment

@pytest.fixture
def sample_patient(db_session, sample_user):
    """Create a sample patient for testing."""
    patient = Patient(
        user_id=sample_user.id,
        medical_history="No significant history",
        allergies="None",
        emergency_contact="123-456-7890"
    )
    db_session.add(patient)
    db_session.commit()
    return patient