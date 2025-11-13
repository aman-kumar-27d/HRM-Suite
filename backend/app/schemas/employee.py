from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    department_id: Optional[str] = None
    role_id: Optional[str] = None
    doj: Optional[str] = None  # ISO date string
    status: Optional[str] = Field(default="active")
    base_salary: Optional[float] = None
    bank_account_id: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[str] = None
    role_id: Optional[str] = None
    doj: Optional[str] = None
    status: Optional[str] = None
    base_salary: Optional[float] = None
    bank_account_id: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

