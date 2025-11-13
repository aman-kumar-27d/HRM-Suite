from typing import Optional
from pydantic import BaseModel, Field


class LeaveTypeBase(BaseModel):
    name: str
    accrual_rule: Optional[str] = None


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeOut(LeaveTypeBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


class LeaveRequestBase(BaseModel):
    employee_id: str
    type_id: str
    start_date: str
    end_date: str
    status: str = "pending"
    reason: Optional[str] = None


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(BaseModel):
    status: Optional[str] = None


class LeaveRequestOut(LeaveRequestBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

