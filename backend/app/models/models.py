from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

db = SQLAlchemy()

class PatientInfo(db.Model):
    __tablename__ = 'PatientInfo'
    Patient_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    ID_number = db.Column(db.Text, unique=True, nullable=False)
    Phone_number = db.Column(db.Integer, nullable=False)
    under_treatment = db.Column(db.Boolean, nullable=False, default=False)
    treatment_ID = db.Column(db.Integer, db.ForeignKey('TreatmentInfo.Treatment_ID'))

class DentistInfo(db.Model):
    __tablename__ = 'DentistInfo'
    Dentist_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text, nullable=False)
    ID_number = db.Column(db.Text, unique=True, nullable=False)
    Phone_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Text, nullable=False)

class TreatmentInfo(db.Model):
    __tablename__ = 'TreatmentInfo'
    Treatment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


class AppointmentInfo(db.Model):
    __tablename__ = 'AppointmentInfo'
    Appointment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Time = db.Column(db.Time, nullable=False)
    Patient_ID = db.Column(db.Integer, db.ForeignKey('PatientInfo.Patient_ID'), nullable=False)
    Treatment_ID = db.Column(db.Integer, db.ForeignKey('TreatmentInfo.Treatment_ID'), nullable=False)
    Dentist_ID = db.Column(db.Integer, db.ForeignKey('DentistInfo.Dentist_ID'), nullable=False)
    # Relationships
    dentist = db.relationship('DentistInfo', backref='appointments')
    treat = db.relationship('TreatmentInfo', backref='appointments')
    patient = db.relationship('PatientInfo', backref='appointments')

class DentistSchedule(db.Model):
    __tablename__ = 'DentistSchedule'
    Schedule_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Dentist_ID = db.Column(db.Integer, db.ForeignKey('DentistInfo.Dentist_ID'), nullable=False)
    Day = db.Column(db.Text, nullable=False)  # e.g., 'Monday', 'Tuesday', etc.
    Start_Time = db.Column(db.Time, nullable=False)
    End_Time = db.Column(db.Time, nullable=False)
