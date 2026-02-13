from flask import Blueprint, request, jsonify
from models import Patient
from extensions import db

patient_bp = Blueprint("patient_bp", __name__)


# CREATE PATIENT
@patient_bp.route("/patients", methods=["POST"])
def add_patient():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    patient = Patient(
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        phone=data["phone"]
    )

    db.session.add(patient)
    db.session.commit()

    return jsonify({
        "message": "Patient added successfully",
        "patient_id": patient.id
    }), 201


# GET ALL PATIENTS
@patient_bp.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()

    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "phone": p.phone
        })

    return jsonify(result), 200


# UPDATE PATIENT
@patient_bp.route("/patients/<int:id>", methods=["PUT"])
def update_patient(id):
    patient = Patient.query.get(id)

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()

    patient.name = data.get("name", patient.name)
    patient.age = data.get("age", patient.age)
    patient.gender = data.get("gender", patient.gender)
    patient.phone = data.get("phone", patient.phone)

    db.session.commit()

    return jsonify({"message": "Patient updated successfully"}), 200


# DELETE PATIENT
@patient_bp.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()

    return jsonify({"message": "Patient deleted successfully"}), 200
