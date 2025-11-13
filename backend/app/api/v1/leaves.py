from typing import List
import asyncio
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from ...schemas.leaves import (
    LeaveTypeCreate,
    LeaveTypeOut,
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestOut,
)


router = APIRouter(prefix="/api/v1", tags=["leaves"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/leave-types", response_model=List[LeaveTypeOut])
async def list_leave_types(db=Depends(get_db)):
    docs = await asyncio.to_thread(lambda: list(db.leave_types.find({})))
    items = []
    for doc in docs:
        doc["_id"] = str(doc["_id"]) 
        items.append(LeaveTypeOut.model_validate(doc))
    return items


@router.post("/leave-types", response_model=LeaveTypeOut)
async def create_leave_type(payload: LeaveTypeCreate, db=Depends(get_db)):
    doc = payload.model_dump()
    res = await asyncio.to_thread(lambda: db.leave_types.insert_one(doc))
    saved = await asyncio.to_thread(lambda: db.leave_types.find_one({"_id": res.inserted_id}))
    saved["_id"] = str(saved["_id"]) 
    return LeaveTypeOut.model_validate(saved)


@router.get("/leaves", response_model=List[LeaveRequestOut])
async def list_leave_requests(db=Depends(get_db)):
    docs = await asyncio.to_thread(lambda: list(db.leave_requests.find({})))
    items = []
    for doc in docs:
        doc["_id"] = str(doc["_id"]) 
        items.append(LeaveRequestOut.model_validate(doc))
    return items


@router.post("/leaves", response_model=LeaveRequestOut)
async def create_leave_request(payload: LeaveRequestCreate, db=Depends(get_db)):
    doc = payload.model_dump()
    res = await asyncio.to_thread(lambda: db.leave_requests.insert_one(doc))
    saved = await asyncio.to_thread(lambda: db.leave_requests.find_one({"_id": res.inserted_id}))
    saved["_id"] = str(saved["_id"]) 
    return LeaveRequestOut.model_validate(saved)


@router.put("/leaves/{id}", response_model=LeaveRequestOut)
async def update_leave_request(id: str, payload: LeaveRequestUpdate, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    update_doc = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    res = await asyncio.to_thread(lambda: db.leave_requests.update_one({"_id": oid}, {"$set": update_doc}))
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Leave request not found")
    doc = await asyncio.to_thread(lambda: db.leave_requests.find_one({"_id": oid}))
    doc["_id"] = str(doc["_id"]) 
    return LeaveRequestOut.model_validate(doc)

