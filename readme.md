Here is a clean, professional, human-written `README.md` without emojis and written in a natural style.

You can copy and paste this directly into your `README.md` file.

---

# Hospital Appointment System (Flask API)

## Overview

The Hospital Appointment System is a backend REST API built using Flask and SQLAlchemy.
It allows hospitals or clinics to manage doctors, patients, and appointment bookings efficiently.

The system includes full CRUD operations for doctors and patients, appointment booking with time-slot validation, prevention of double booking, appointment status management, filtering options, and audit logging.

---

## Features

### Doctor Management

* Create doctor
* View all doctors
* View doctor by ID
* Update doctor
* Delete doctor

### Patient Management

* Create patient
* View all patients
* Update patient
* Delete patient

### Appointment Management

* Book appointment with validation
* Prevent overlapping appointments
* View all appointments
* Filter appointments by doctor and date
* Update appointment status (Booked, Cancelled, Completed)
* Delete appointment

### Audit Logging

All important operations such as doctor creation, appointment booking, status updates, and deletions are logged in a file named `audit.log`.

---

## Technology Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite (default database)

---

## Project Structure

```
Health Care management/
│
├── app.py
├── extensions.py
├── models.py
├── audit_logger.py
├── audit.log
│
└── routes/
    ├── __init__.py
    ├── doctor_routes.py
    ├── patient_routes.py
    └── appointment_routes.py
```

---

## Required Modules

Install the following modules before running the project:

```
pip install flask flask-sqlalchemy
```

Optional modules:

For database migrations:

```
pip install flask-migrate
```

For environment variable management:

```
pip install python-dotenv
```

Recommended complete installation:

```
pip install flask flask-sqlalchemy flask-migrate python-dotenv
```

---

## How to Run the Project

### Step 1: Navigate to the project directory

```
cd "D:\New folder\Health Care management\Health Care management"
```

### Step 2: Create a virtual environment

```
python -m venv venv
```

### Step 3: Activate the virtual environment

PowerShell:

```
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```
venv\Scripts\activate.bat
```

### Step 4: Install dependencies

```
pip install flask flask-sqlalchemy
```

### Step 5: Run the application

```
python app.py
```

The server will run at:

```
http://127.0.0.1:5000
```

---

## API Endpoints

Base URL:

```
http://127.0.0.1:5000
```

---

## Doctor APIs

Create Doctor
POST

```
http://127.0.0.1:5000/doctors
```

Request Body:

```json
{
  "name": "Dr. Kumar",
  "specialization": "Cardiology",
  "available_from": "09:00",
  "available_to": "17:00"
}
```

List Doctors
GET

```
http://127.0.0.1:5000/doctors
```

Get Doctor by ID
GET

```
http://127.0.0.1:5000/doctors/1
```

Update Doctor
PUT

```
http://127.0.0.1:5000/doctors/1
```

Delete Doctor
DELETE

```
http://127.0.0.1:5000/doctors/1
```

---

## Patient APIs

Create Patient
POST

```
http://127.0.0.1:5000/patients
```

Request Body:

```json
{
  "name": "Aakash",
  "age": 22,
  "gender": "Male",
  "phone": "9876543210"
}
```

List Patients
GET

```
http://127.0.0.1:5000/patients
```

Update Patient
PUT

```
http://127.0.0.1:5000/patients/1
```

Delete Patient
DELETE

```
http://127.0.0.1:5000/patients/1
```

---

## Appointment APIs

Book Appointment
POST

```
http://127.0.0.1:5000/appointments
```

Request Body:

```json
{
  "doctor_id": 1,
  "patient_id": 1,
  "appointment_date": "2026-02-15",
  "start_time": "10:00",
  "end_time": "10:30"
}
```

List Appointments
GET

```
http://127.0.0.1:5000/appointments
```

Filter Appointments
GET

```
http://127.0.0.1:5000/appointments?doctor_id=1&date=2026-02-15
```

Update Appointment Status
PUT

```
http://127.0.0.1:5000/appointments/1/status
```

Request Body:

```json
{
  "status": "Cancelled"
}
```

Allowed Status Values:

* Booked
* Cancelled
* Completed

Delete Appointment
DELETE

```
http://127.0.0.1:5000/appointments/1
```

---

## Important Notes

* Appointment booking includes time validation and overlap checking.
* The database used is SQLite by default.
* If database models are modified, delete the existing `hospital.db` file and restart the application to recreate tables.
* This is a development server and not recommended for production use.

