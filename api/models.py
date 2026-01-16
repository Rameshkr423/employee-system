from pydantic import BaseModel
from datetime import date

class EmployeeCreate(BaseModel):
    emp_id: str
    name: str
    email: str
    mobile: str
    role: str
    doj: str

class LoginRequest(BaseModel):
    user_id: str
    role: str  # EMPLOYEE / HR

class LeaveRequest(BaseModel):
    emp_id: str
    date: date
    reason: str
