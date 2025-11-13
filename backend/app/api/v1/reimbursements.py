from typing import List
import asyncio
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from ...schemas.reimbursements import (
    ReimbursementCreate,
    ReimbursementUpdate,
    ReimbursementOut,
)


router = APIRouter(prefix="/api/v1/reimbursements", tags=["reimbursements"])


def get_db(request: Request):
    db = getattr(request.app.state, "db", None)
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/", response_model=List[ReimbursementOut])
async def list_reimbursements(db=Depends(get_db)):
    docs = await asyncio.to_thread(lambda: list(db.reimbursements.find({})))
    items = []
    for doc in docs:
        doc["__id"] = str(doc["_id"]) 
        items.append(ReimbursementOut.model_validate(doc))
    return items


@router.post("/", response_model=ReimbursementOut)
async def create_reimbursement(payload: ReimbursementCreate, db=Depends(get_db)):
    doc = payload.model_dump()
    res = await asyncio.to_thread(lambda: db.reimbursements.insert_one(doc))
    saved = await asyncio.to_thread(lambda: db.reimbursements.find_one({"_id": res.inserted_id}))
    saved["_id"] = str(saved["_id"]) 
    return ReimbursementOut.model_validate(saved)


@router.put("/{id}", response_model=ReimbursementOut)
async def update_reimbursement(id: str, payload: ReimbursementUpdate, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    update_doc = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    res = await asyncio.to_thread(lambda: db.reimbursements.update_one({"_id": oid}, {"$set": update_doc}))
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reimbursement not found")
    doc = await asyncio.to_thread(lambda: db.reimbursements.find_one({"_id": oid}))
    doc["_id"] = str(doc["_id"]) 
    return ReimbursementOut.model_validate(doc)

