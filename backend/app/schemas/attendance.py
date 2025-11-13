from typing import Optional
from pydantic import BaseModel, Field


class AttendanceBase(BaseModel):
    employee_id: str
    date: str
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    hours: Optional[float] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceOut(AttendanceBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

