from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List

class EmployeeRegisterRequest(BaseModel):
    emp_id: str = Field(..., example="EMP001")
    name: str = Field(..., example="Arun Kumar")
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    role: str = Field(..., example="DEVELOPER")
    doj: date
    manager_id: Optional[str] = None
    active: bool = True


class LoginRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)


class RoleCreateRequest(BaseModel):
    role_id: str = Field(..., example="DEVELOPER")
    role_name: str = Field(..., example="Software Developer")
    permissions: List[str] = Field(
        default_factory=list,
        example=["VIEW_PROJECT", "APPLY_LEAVE"]
    )


class RoleResponse(BaseModel):
    role_id: str
    role_name: str
    permissions: List[str]


class ProjectCreateRequest(BaseModel):
    project_id: str = Field(..., example="PRJ001")
    name: str = Field(..., example="Employee Management System")
    description: Optional[str] = None
    status: str = Field(default="ACTIVE")  # ACTIVE / CLOSED
    start_date: date
    end_date: Optional[date] = None


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: Optional[str]
    status: str
    start_date: date
    end_date: Optional[date]



class ProjectAssignRequest(BaseModel):
    emp_id: str = Field(..., example="EMP001")
    project_id: str = Field(..., example="PRJ001")



class LeaveApplyRequest(BaseModel):
    emp_id: str = Field(..., example="EMP001")
    from_date: date
    to_date: date
    reason: str
    status: str = Field(
        default="PENDING",
        description="PENDING | APPROVED | REJECTED | CANCELLED"
    )



class LeaveStatusUpdateRequest(BaseModel):
    leave_id: str
    status: str = Field(..., example="APPROVED")
    remarks: Optional[str] = None


class LeaveRequest(BaseModel):
    emp_id: str
    date: date
    reason: str
