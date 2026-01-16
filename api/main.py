from fastapi import FastAPI, HTTPException
from datetime import datetime

from api.models import EmployeeCreate, LoginRequest, LeaveRequest
from api.firestore_db import (
    create_user, save_employee, get_employee, list_employees, mark_leave
)
from api.pubsub_publisher import publish_event
from api.auth import login

app = FastAPI(title="Employee Management System")

@app.get("/")
def root():
    return {
        "service": "Employee Management System",
        "status": "running"
    }

# ---------- LOGIN ----------
@app.post("/login")
def user_login(data: LoginRequest):
    if not login(data.user_id, data.role):
        raise HTTPException(status_code=401, detail="Invalid login")
    return {"status": "Login successful"}


# ---------- REGISTER EMPLOYEE ----------
@app.post("/employee/register")
def register_employee(emp: EmployeeCreate):
    employee = emp.dict()

    # Save employee profile
    save_employee(employee)

    # Create login user
    create_user({
        "user_id": emp.emp_id,
        "role": emp.role
    })

    # Publish event
    publish_event("EMPLOYEE_CREATED", employee)

    return {"status": "Employee registered"}


# ---------- VIEW EMPLOYEE ----------
@app.get("/employee/{emp_id}")
def view_employee(emp_id: str):
    emp = get_employee(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# ---------- HR: LIST EMPLOYEES ----------
@app.get("/hr/employees")
def hr_list_employees():
    return list_employees()


# ---------- HR: MARK LEAVE ----------
@app.post("/hr/leave")
def hr_mark_leave(data: LeaveRequest):
    leave = {
        "emp_id": data.emp_id,
        "date": str(data.date),
        "reason": data.reason,
        "marked_at": datetime.utcnow().isoformat()
    }

    mark_leave(leave)

    publish_event("LEAVE_MARKED", leave)

    return {"status": "Leave marked"}
