from datetime import datetime
from extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    available_from = db.Column(db.Time, nullable=False)
    available_to = db.Column(db.Time, nullable=False)

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    appointments = db.relationship("Appointment", backref="patient", lazy=True)


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),   # fixed
        nullable=False
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),  # fixed
        nullable=False
    )

    appointment_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    status = db.Column(db.String(20), default="Booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
