import asyncio
import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import StreamingResponse


router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/payroll")
async def payroll_summary(from_date: str, to_date: str, db=Depends(get_db)):
    pipeline = [
        {"$match": {"processed_at": {"$exists": True}}},
    ]
    runs = await asyncio.to_thread(lambda: list(db.payroll_runs.aggregate(pipeline)))
    return {"runs": len(runs)}


@router.get("/attendance")
async def attendance_summary(from_date: str, to_date: str, db=Depends(get_db)):
    pipeline = [
        {"$match": {"date": {"$gte": from_date, "$lte": to_date}}},
        {"$group": {"_id": "$employee_id", "hours": {"$sum": {"$ifNull": ["$hours", 0]}}}},
    ]
    docs = await asyncio.to_thread(lambda: list(db.attendance.aggregate(pipeline)))
    for d in docs:
        d["employee_id"] = d.pop("_id")
    return {"summary": docs}


@router.get("/reimbursements")
async def reimbursements_summary(from_date: str, to_date: str, db=Depends(get_db)):
    pipeline = [
        {"$match": {"date": {"$gte": from_date, "$lte": to_date}, "status": "approved"}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
    ]
    docs = await asyncio.to_thread(lambda: list(db.reimbursements.aggregate(pipeline)))
    for d in docs:
        d["category"] = d.pop("_id")
    return {"summary": docs}


@router.get("/export.csv")
async def export_csv(type: str, from_date: str, to_date: str, db=Depends(get_db)):
    buffer = StringIO()
    writer = csv.writer(buffer)
    if type == "attendance":
        writer.writerow(["employee_id", "hours"])
        pipeline = [
            {"$match": {"date": {"$gte": from_date, "$lte": to_date}}},
            {"$group": {"_id": "$employee_id", "hours": {"$sum": {"$ifNull": ["$hours", 0]}}}},
        ]
        rows = await asyncio.to_thread(lambda: list(db.attendance.aggregate(pipeline)))
        for r in rows:
            writer.writerow([r["_id"], r.get("hours", 0)])
    elif type == "reimbursements":
        writer.writerow(["category", "total"])
        pipeline = [
            {"$match": {"date": {"$gte": from_date, "$lte": to_date}, "status": "approved"}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        ]
        rows = await asyncio.to_thread(lambda: list(db.reimbursements.aggregate(pipeline)))
        for r in rows:
            writer.writerow([r["_id"], r.get("total", 0)])
    elif type == "payroll":
        writer.writerow(["employee_id", "gross", "deductions", "reimbursements", "net"])
        rows = await asyncio.to_thread(lambda: list(db.payroll_items.find({})))
        for r in rows:
            writer.writerow([str(r.get("employee_id")), r.get("gross", 0), r.get("deductions", 0), r.get("reimbursements", 0), r.get("net", 0)])
    else:
        raise HTTPException(status_code=400, detail="Invalid type")
    buffer.seek(0)
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv")

