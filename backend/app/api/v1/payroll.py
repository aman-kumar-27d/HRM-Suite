import asyncio
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from ...services.payroll import compute_payroll_items, generate_payslip_html


router = APIRouter(prefix="/api/v1/payroll", tags=["payroll"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.post("/run")
async def run_payroll(period_start: str, period_end: str, db=Depends(get_db)):
    items = await compute_payroll_items(db, period_start, period_end)
    run_doc = {
        "period_start": period_start,
        "period_end": period_end,
        "status": "computed",
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }
    run_res = await asyncio.to_thread(lambda: db.payroll_runs.insert_one(run_doc))
    run_id = run_res.inserted_id
    for item in items:
        item["payroll_run_id"] = run_id
    await asyncio.to_thread(lambda: db.payroll_items.insert_many(items))
    employees = await asyncio.to_thread(lambda: list(db.employees.find({})))
    emp_map = {str(e["_id"]): e for e in employees}
    payslips = []
    for item in items:
        emp = emp_map.get(item["employee_id"], {})
        html = generate_payslip_html(item, emp)
        payslips.append({
            "payroll_item_id": item.get("_id") or None,
            "payroll_run_id": run_id,
            "html_snapshot": html,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        })
    if payslips:
        await asyncio.to_thread(lambda: db.payslips.insert_many(payslips))
    return {"run_id": str(run_id), "items_count": len(items)}


@router.post("/payout")
async def payout(run_id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(run_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid run_id")
    items = await asyncio.to_thread(lambda: list(db.payroll_items.find({"payroll_run_id": oid})))
    if not items:
        raise HTTPException(status_code=404, detail="No payroll items for run")
    for item in items:
        ref = f"MOCK-{str(item.get('_id'))}"
        await asyncio.to_thread(lambda: db.payroll_items.update_one({"_id": item["_id"]}, {"$set": {"payout_ref": ref}}))
    await asyncio.to_thread(lambda: db.payroll_runs.update_one({"_id": oid}, {"$set": {"status": "paid"}}))
    return {"paid_count": len(items)}


@router.get("/payslips")
async def list_payslips(run_id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(run_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid run_id")
    docs = await asyncio.to_thread(lambda: list(db.payslips.find({"payroll_run_id": oid})))
    for d in docs:
        d["_id"] = str(d["_id"]) 
        d["payroll_run_id"] = str(d["payroll_run_id"]) 
        if d.get("payroll_item_id"):
            d["payroll_item_id"] = str(d["payroll_item_id"]) 
    return docs

