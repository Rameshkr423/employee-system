from google.cloud import firestore
db = firestore.Client()

def create_user(user):
    db.collection("users").document(user["user_id"]).set(user)

def get_user(user_id):
    doc = db.collection("users").document(user_id).get()
    return doc.to_dict() if doc.exists else None

def save_employee(emp):
    db.collection("employees").document(emp["emp_id"]).set(emp)

def get_employee(emp_id):
    doc = db.collection("employees").document(emp_id).get()
    return doc.to_dict() if doc.exists else None

def list_employees():
    return [d.to_dict() for d in db.collection("employees").stream()]

def mark_leave(leave):
    db.collection("leaves").add(leave)
