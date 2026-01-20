from fastapi import FastAPI, HTTPException
from datetime import datetime
from google.cloud import firestore

from api.models import (
    EmployeeRegisterRequest,
    LoginRequest,
    ProjectCreateRequest,
    ProjectAssignRequest,
    LeaveApplyRequest
)

from api.firestore_db import (
    create_user,
    save_employee,
    get_employee,
    list_employees,
    get_user_by_mobile,
    hash_password,
    verify_password,
    is_email_or_mobile_exists
)

from api.pubsub_publisher import publish_event

# Firestore direct client (for projects & assignments)
db = firestore.Client()

app = FastAPI(title="Employee Management System")
@app.get("/")
def root():
    return {
        "service": "Employee API",
        "status": "running"
    }


@app.post("/login")
def login_api(data: LoginRequest):

    user = get_user_by_mobile(data.mobile)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User account disabled")

    return {
        "status": "success",
        "emp_id": user["emp_id"],
        "role": user["role"]
    }


@app.post("/employee/register")
def register_employee(data: EmployeeRegisterRequest):

    if is_email_or_mobile_exists(data.email, data.mobile):
        raise HTTPException(
            status_code=400,
            detail="Email or mobile already exists"
        )

    employee = {
        "emp_id": data.emp_id,
        "name": data.name,
        "email": data.email,
        "mobile": data.mobile,
        "role": data.role,
        "doj": data.doj.isoformat(),
        "manager_id": data.manager_id,
        "active": data.active,
        "created_at": datetime.utcnow().isoformat()
    }

    save_employee(employee)

    user = {
        "emp_id": data.emp_id,
        "email": data.email,
        "mobile": data.mobile,
        "password_hash": hash_password(data.password),
        "role": data.role,
        "active": data.active,
        "created_at": datetime.utcnow().isoformat()
    }

    create_user(user)

    publish_event("EMPLOYEE_CREATED", employee)

    return {
        "status": "success",
        "message": "Employee registered successfully"
    }

@app.get("/hr/employees")
def hr_list_employees():
    return list_employees()

@app.get("/employee/{emp_id}")
def view_employee(emp_id: str):

    emp = get_employee(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return emp

@app.post("/projects")
def create_project(data: ProjectCreateRequest):

    project = {
        "project_id": data.project_id,
        "name": data.name,
        "description": data.description,
        "status": data.status,
        "start_date": data.start_date.isoformat(),
        "end_date": data.end_date.isoformat() if data.end_date else None,
        "created_at": datetime.utcnow().isoformat()
    }

    db.collection("projects").document(data.project_id).set(project)
    publish_event("PROJECT_CREATED", project)

    return {"status": "success", "message": "Project created"}

@app.get("/projects")
def list_projects():
    return [doc.to_dict() for doc in db.collection("projects").stream()]

@app.put("/projects/{project_id}")
def update_project(project_id: str, data: ProjectCreateRequest):

    ref = db.collection("projects").document(project_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Project not found")

    updated_data = {
        "project_id": project_id,
        "name": data.name,
        "description": data.description,
        "status": data.status,
        "start_date": data.start_date.isoformat(),
        "end_date": data.end_date.isoformat() if data.end_date else None,
        "updated_at": datetime.utcnow().isoformat()
    }

    ref.update(updated_data)

        # ✅ Correct publish payload
    publish_event("PROJECT_UPDATED", updated_data)

    return {"status": "success", "message": "Project updated"}

@app.delete("/projects/{project_id}")
def delete_project(project_id: str):


    ref = db.collection("projects").document(project_id)
    snapshot = ref.get()

    if not snapshot.exists:
        raise HTTPException(status_code=404, detail="Project not found")

    ref.delete()

    # ✅ Always send structured payload
    publish_event(
        "PROJECT_DELETED",
        {
            "project_id": project_id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    )


    return {"status": "success", "message": "Project deleted"}

@app.post("/projects/assign")
def assign_project(data: ProjectAssignRequest):

    assignment = {
        "emp_id": data.emp_id,
        "project_id": data.project_id,
        "assigned_at": datetime.utcnow().isoformat()
    }

    db.collection("project_assignments").add(assignment)
    publish_event("PROJECT_ASSIGNED", assignment)

    return {"status": "success", "message": "Project assigned"}


@app.post("/leave/apply")
def apply_leave(data: LeaveApplyRequest):

    leave = {
        "emp_id": data.emp_id,
        "from_date": data.from_date.isoformat(),
        "to_date": data.to_date.isoformat(),
        "reason": data.reason,
        "status": data.status,
        "applied_at": datetime.utcnow().isoformat()
    }

    db.collection("leaves").add(leave)
    publish_event("LEAVE_APPLIED", leave)

    return {"status": "success", "message": "Leave applied"}
