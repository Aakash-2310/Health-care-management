from flask import Blueprint, request, jsonify
from datetime import datetime
from extensions import db
from models import Doctor
from audit_logger import audit

doctor_bp = Blueprint("doctor_bp", __name__)

def parse_time(t: str):
    return datetime.strptime(t, "%H:%M").time()

@doctor_bp.route("/doctors", methods=["POST"])
def create_doctor():
    data = request.get_json()

    doctor = Doctor(
        name=data["name"],
        specialization=data.get("specialization"),
        available_from=parse_time(data["available_from"]),
        available_to=parse_time(data["available_to"]),
    )
    db.session.add(doctor)
    db.session.commit()

    audit("DOCTOR_CREATED", f"doctor_id={doctor.id}, name={doctor.name}")
    return jsonify({"message": "Doctor created", "doctor_id": doctor.id}), 201


@doctor_bp.route("/doctors", methods=["GET"])
def list_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        "id": d.id,
        "name": d.name,
        "specialization": d.specialization,
        "available_from": str(d.available_from),
        "available_to": str(d.available_to),
    } for d in doctors]), 200


@doctor_bp.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    d = Doctor.query.get(doctor_id)
    if not d:
        return jsonify({"error": "Doctor not found"}), 404

    return jsonify({
        "id": d.id,
        "name": d.name,
        "specialization": d.specialization,
        "available_from": str(d.available_from),
        "available_to": str(d.available_to),
    }), 200


@doctor_bp.route("/doctors/<int:doctor_id>", methods=["PUT"])
def update_doctor(doctor_id):
    d = Doctor.query.get(doctor_id)
    if not d:
        return jsonify({"error": "Doctor not found"}), 404

    data = request.get_json()
    d.name = data.get("name", d.name)
    d.specialization = data.get("specialization", d.specialization)

    if "available_from" in data:
        d.available_from = parse_time(data["available_from"])
    if "available_to" in data:
        d.available_to = parse_time(data["available_to"])

    db.session.commit()
    audit("DOCTOR_UPDATED", f"doctor_id={d.id}")
    return jsonify({"message": "Doctor updated"}), 200


@doctor_bp.route("/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    d = Doctor.query.get(doctor_id)
    if not d:
        return jsonify({"error": "Doctor not found"}), 404

    db.session.delete(d)
    db.session.commit()

    audit("DOCTOR_DELETED", f"doctor_id={doctor_id}")
    return jsonify({"message": "Doctor deleted"}), 200
