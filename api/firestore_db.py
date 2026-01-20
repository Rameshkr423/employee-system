from google.cloud import firestore
from passlib.context import CryptContext
from datetime import datetime

db = firestore.Client()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_user(user: dict):
    db.collection("users").document(user["emp_id"]).set(user)

def get_user(emp_id: str):
    doc = db.collection("users").document(emp_id).get()
    return doc.to_dict() if doc.exists else None

def get_user_by_mobile(mobile: str):
    docs = db.collection("users").where("mobile", "==", mobile).stream()
    for doc in docs:
        return doc.to_dict()
    return None

def is_email_or_mobile_exists(email: str, mobile: str) -> bool:
    email_docs = db.collection("users").where("email", "==", email).stream()
    mobile_docs = db.collection("users").where("mobile", "==", mobile).stream()
    return any(email_docs) or any(mobile_docs)

def save_employee(emp: dict):
    db.collection("employees").document(emp["emp_id"]).set(emp)

def get_employee(emp_id: str):
    doc = db.collection("employees").document(emp_id).get()
    return doc.to_dict() if doc.exists else None

def list_employees():
    return [doc.to_dict() for doc in db.collection("employees").stream()]

def create_project(project: dict):
    db.collection("projects").document(project["project_id"]).set(project)

def get_project(project_id: str):
    doc = db.collection("projects").document(project_id).get()
    return doc.to_dict() if doc.exists else None

def list_projects():
    return [doc.to_dict() for doc in db.collection("projects").stream()]

def update_project(project_id: str, data: dict):
    db.collection("projects").document(project_id).update(data)

def delete_project(project_id: str):
    db.collection("projects").document(project_id).delete()

def assign_project(assignment: dict):
    db.collection("project_assignments").add(assignment)

def apply_leave(leave: dict):
    db.collection("leaves").add(leave)

def list_leaves_by_employee(emp_id: str):
    return [
        doc.to_dict()
        for doc in db.collection("leaves")
        .where("emp_id", "==", emp_id)
        .stream()
    ]
