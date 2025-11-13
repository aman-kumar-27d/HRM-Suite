from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut


router = APIRouter(prefix="/api/v1/employees", tags=["employees"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/", response_model=List[EmployeeOut])
async def list_employees(db=Depends(get_db)):
    cursor = db.employees.find({})
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # serialize ObjectId
        items.append(EmployeeOut.model_validate(doc))
    return items


@router.post("/", response_model=EmployeeOut)
async def create_employee(payload: EmployeeCreate, db=Depends(get_db)):
    doc = payload.model_dump()
    res = await db.employees.insert_one(doc)
    saved = await db.employees.find_one({"_id": res.inserted_id})
    saved["_id"] = str(saved["_id"])  # serialize
    return EmployeeOut.model_validate(saved)


@router.get("/{id}", response_model=EmployeeOut)
async def get_employee(id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await db.employees.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    doc["_id"] = str(doc["_id"])  # serialize
    return EmployeeOut.model_validate(doc)


@router.put("/{id}", response_model=EmployeeOut)
async def update_employee(id: str, payload: EmployeeUpdate, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    update_doc = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    res = await db.employees.update_one({"_id": oid}, {"$set": update_doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    doc = await db.employees.find_one({"_id": oid})
    doc["_id"] = str(doc["_id"])  # serialize
    return EmployeeOut.model_validate(doc)


@router.delete("/{id}")
async def delete_employee(id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await db.employees.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True}

