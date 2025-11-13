from typing import Optional
from pydantic import BaseModel, Field


class ReimbursementBase(BaseModel):
    employee_id: str
    category: str
    amount: float
    date: str
    status: str = "pending"
    note: Optional[str] = None


class ReimbursementCreate(ReimbursementBase):
    pass


class ReimbursementUpdate(BaseModel):
    status: Optional[str] = None


class ReimbursementOut(ReimbursementBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

