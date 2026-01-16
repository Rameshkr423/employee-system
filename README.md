Employee Management System (Event-Driven with Google Pub/Sub)

A Python + FastAPI + Firestore + Google Pub/Sub based event-driven employee management system designed to demonstrate real-world Pub/Sub usage.

This project covers:

Employee registration

HR & Employee roles

Attendance & leave workflows

Event publishing using Pub/Sub

Asynchronous event processing via subscriber

🚀 Tech Stack

Python 3.11

FastAPI – REST API

Google Cloud Firestore – NoSQL Database

Google Cloud Pub/Sub – Event messaging

Pydantic – Request validation

Uvicorn – ASGI server



Client (Swagger / Postman)
        |
        v
FastAPI (Employee API)
        |
        |  Publish Event
        v
Google Pub/Sub Topic
        |
        v
Subscriber Service
        |
        v
Firestore (events / audit / async data)



Project Folder :


employee-system/
│
├── api/
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Pydantic models
│   ├── firestore_db.py      # Firestore operations
│   ├── pubsub_publisher.py  # Pub/Sub publisher
│   └── auth.py              # Simple auth logic
│
├── subscriber/
│   └── main.py              # Pub/Sub subscriber
│
├── requirements.txt
└── README.md


🗄 Firestore Collections
Collection	Purpose
employees	Employee master data
users	Login users (employee / HR)
attendance	Attendance records
leaves	Leave records
events	Pub/Sub audit events


📦 Requirements
fastapi
uvicorn
pydantic
google-cloud-firestore
google-cloud-pubsub

🔧 Setup Instructions (Step-by-Step)
1️⃣ Clone Repository
git clone https://github.com/your-username/employee-system.git
cd employee-system

2️⃣ Use Python 3.11
python --version


Output must be:

Python 3.11.x

3️⃣ Create Virtual Environment
python -m venv venv


Activate:

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Authenticate with Google Cloud
gcloud auth application-default login


This allows:

Firestore access

Pub/Sub access

6️⃣ Create Pub/Sub Topic & Subscription
gcloud pubsub topics create employee-events
gcloud pubsub subscriptions create employee-events-sub \
  --topic employee-events

▶️ Running the Application
1️⃣ Start FastAPI Server
uvicorn api.main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

2️⃣ Start Pub/Sub Subscriber (New Terminal)
venv\Scripts\activate
python subscriber/main.py


Output:

Subscriber running... (Press CTRL+C to stop)

🧪 API Usage
✅ Register Employee
POST /employee/register

{
  "emp_id": "EMP0001",
  "name": "Ramesh KR",
  "email": "ramesh@gmail.com",
  "mobile": "9876543210",
  "role": "EMPLOYEE",
  "doj": "2026-01-16"
}


✔ Stored in Firestore
✔ Event published to Pub/Sub
✔ Subscriber receives event

✅ Mark Attendance
POST /attendance/mark

{
  "emp_id": "EMP0001",
  "date": "2026-01-16",
  "status": "PRESENT"
}

✅ HR – Mark Leave
POST /hr/leave

{
  "emp_id": "EMP0001",
  "date": "2026-01-20",
  "reason": "Personal"
}

🔔 Pub/Sub Events
Event Type	Trigger
EMPLOYEE_CREATED	Employee registered
ATTENDANCE_MARKED	Attendance marked
LEAVE_MARKED	Leave marked

Each event is:

Published by API

Consumed by subscriber

Stored in Firestore (events)

🧠 Why Pub/Sub is Used Here

Without Pub/Sub ❌:

API becomes slow

Tight coupling

Hard to scale

With Pub/Sub ✅:

Async processing

Loose coupling

Multiple subscribers possible

Production-ready architecture

🧪 Verify Pub/Sub Working

Keep subscriber running

Register employee or mark attendance

Subscriber prints:

Event received: EMPLOYEE_CREATED


Check Firestore → events collection

🔐 Security Notes

Local uses Application Default Credentials

Production should use Service Accounts

IAM roles required:

Firestore User

Pub/Sub Publisher / Subscriber

🚀 Future Enhancements

JWT authentication

Role-based access (HR vs Employee)

Email / WhatsApp notifications

Dead Letter Topic (DLQ)

Cloud Run deployment

Multiple subscribers

Payroll integration

📌 Learning Outcomes

This project demonstrates:

Real Pub/Sub usage (not demo)

Event-driven system design

Clean FastAPI structure

Cloud-native thinking