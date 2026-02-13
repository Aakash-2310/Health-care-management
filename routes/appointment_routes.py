from flask import Blueprint, request, jsonify
from datetime import datetime, date
from extensions import db
from models import Appointment, Doctor, Patient
from audit_logger import audit

appointment_bp = Blueprint("appointment_bp", __name__)

ALLOWED_STATUSES = {"Booked", "Cancelled", "Completed"}

def parse_date(d: str):
    return datetime.strptime(d, "%Y-%m-%d").date()

def parse_time(t: str):
    return datetime.strptime(t, "%H:%M").time()

def to_dict(a: Appointment):
    return {
        "id": a.id,
        "doctor_id": a.doctor_id,
        "patient_id": a.patient_id,
        "appointment_date": str(a.appointment_date),
        "start_time": str(a.start_time),
        "end_time": str(a.end_time),
        "status": a.status,
        "created_at": a.created_at.isoformat()
    }


@appointment_bp.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()

    doctor = Doctor.query.get(data["doctor_id"])
    patient = Patient.query.get(data["patient_id"])
    if not doctor or not patient:
        return jsonify({"error": "Doctor or Patient not found"}), 404

    appt_date = parse_date(data["appointment_date"])
    start = parse_time(data["start_time"])
    end = parse_time(data["end_time"])

    
    if appt_date < date.today():
        return jsonify({"error": "Appointment date cannot be in the past"}), 400
    if start >= end:
        return jsonify({"error": "start_time must be less than end_time"}), 400

  
    if start < doctor.available_from or end > doctor.available_to:
        return jsonify({"error": "Outside doctor's available time"}), 400

   
    existing = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == appt_date,
        Appointment.status == "Booked",
        Appointment.start_time < end,
        Appointment.end_time > start
    ).first()

    if existing:
        return jsonify({"error": "Time slot already booked"}), 400

    appt = Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        appointment_date=appt_date,
        start_time=start,
        end_time=end,
        status="Booked"
    )

    db.session.add(appt)
    db.session.commit()

    audit("APPOINTMENT_BOOKED", f"appointment_id={appt.id}, doctor_id={doctor.id}, patient_id={patient.id}")
    return jsonify({"message": "Appointment booked successfully", "appointment": to_dict(appt)}), 201



@appointment_bp.route("/appointments", methods=["GET"])
def list_appointments():
    doctor_id = request.args.get("doctor_id", type=int)
    date_str = request.args.get("date")

    query = Appointment.query

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    if date_str:
        try:
            d = parse_date(date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        query = query.filter(Appointment.appointment_date == d)

    appts = query.order_by(Appointment.appointment_date.desc(), Appointment.start_time.asc()).all()
    return jsonify([to_dict(a) for a in appts]), 200



@appointment_bp.route("/appointments/<int:appt_id>/status", methods=["PUT"])
def update_status(appt_id):
    appt = Appointment.query.get(appt_id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ALLOWED_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed: {sorted(ALLOWED_STATUSES)}"}), 400

    if appt.status in {"Completed", "Cancelled"}:
        return jsonify({"error": f"Cannot change status from {appt.status}"}), 400

    appt.status = new_status
    db.session.commit()

    audit("APPOINTMENT_STATUS_UPDATED", f"appointment_id={appt.id}, new_status={new_status}")
    return jsonify({"message": "Status updated", "appointment": to_dict(appt)}), 200



@appointment_bp.route("/appointments/<int:appt_id>", methods=["DELETE"])
def delete_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appt)
    db.session.commit()

    audit("APPOINTMENT_DELETED", f"appointment_id={appt_id}")
    return jsonify({"message": "Appointment deleted"}), 200
