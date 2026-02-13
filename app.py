from flask import Flask, jsonify
from extensions import db

from routes.doctor_routes import doctor_bp
from routes.patient_routes import patient_bp   # keep your patient routes file
from routes.appointment_routes import appointment_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)

    @app.get("/")
    def home():
        return jsonify({"message": "Hospital API running"})

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
