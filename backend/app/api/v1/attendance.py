from typing import List, Optional
import asyncio
import csv
from io import StringIO

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from starlette.requests import Request

from ...schemas.attendance import AttendanceCreate, AttendanceOut


router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/", response_model=List[AttendanceOut])
async def list_attendance(
    employee_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db=Depends(get_db),
):
    query: dict = {}
    if employee_id:
        try:
            query["employee_id"] = str(ObjectId(employee_id))
        except Exception:
            query["employee_id"] = employee_id
    if from_date and to_date:
        query["date"] = {"$gte": from_date, "$lte": to_date}
    docs = await asyncio.to_thread(lambda: list(db.attendance.find(query)))
    items = []
    for doc in docs:
        doc["_id"] = str(doc["_id"]) 
        items.append(AttendanceOut.model_validate(doc))
    return items


@router.post("/", response_model=AttendanceOut)
async def create_attendance(payload: AttendanceCreate, db=Depends(get_db)):
    doc = payload.model_dump()
    res = await asyncio.to_thread(lambda: db.attendance.insert_one(doc))
    saved = await asyncio.to_thread(lambda: db.attendance.find_one({"_id": res.inserted_id}))
    saved["_id"] = str(saved["_id"]) 
    return AttendanceOut.model_validate(saved)


@router.post("/import")
async def import_csv(file: UploadFile = File(...), db=Depends(get_db)):
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    rows = []
    for row in reader:
        item = {
            "employee_id": row.get("employee_id"),
            "date": row.get("date"),
            "check_in": row.get("check_in") or None,
            "check_out": row.get("check_out") or None,
            "hours": float(row.get("hours")) if row.get("hours") else None,
        }
        rows.append(item)
    if rows:
        await asyncio.to_thread(lambda: db.attendance.insert_many(rows))
    return {"inserted": len(rows)}

