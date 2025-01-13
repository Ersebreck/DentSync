"""
Database seeding script for the dental clinic system.
This script populates the database with synthetic data for development and testing.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

import random
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from faker import Faker
from passlib.context import CryptContext

# Now we can import our app modules
from app.db.base import SessionLocal
from app.models.users import User, Role
from app.models.patients import Patient
from app.models.dentists import Dentist
from app.models.treatments import Treatment
from app.models.appointments import Appointment, AppointmentStatus
from app.models.staff import Staff

# Initialize Faker and password hasher
fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rest of your seed_data.py code remains the same
...

def seed_database():
    """Main function to populate the database with synthetic data."""
    print("Starting database seeding process...")
    print(f"Using backend directory: {backend_dir}")
    
    db = SessionLocal()
    try:
        print("Creating roles...")
        roles = create_roles(db)
        
        print("Creating treatments...")
        treatments = create_treatments(db)
        
        print("Creating dentists...")
        dentists = create_dentists(db, roles["dentist"])
        
        print("Creating patients...")
        patients = create_patients(db, roles["patient"])
        
        print("Creating appointments...")
        appointments = create_appointments(db, patients, dentists, treatments)
        
        print("Database seeding completed successfully!")
        print(f"Created:")
        print(f"- {len(treatments)} treatments")
        print(f"- {len(dentists)} dentists")
        print(f"- {len(patients)} patients")
        print(f"- {len(appointments)} appointments")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()