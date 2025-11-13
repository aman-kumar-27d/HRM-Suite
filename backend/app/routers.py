from fastapi import APIRouter
from .api.v1 import api_router as v1

router = APIRouter()
router.include_router(v1)

