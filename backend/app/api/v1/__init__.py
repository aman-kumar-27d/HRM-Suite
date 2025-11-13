from fastapi import APIRouter
from .employees import router as employees_router
from .attendance import router as attendance_router

api_router = APIRouter()
api_router.include_router(employees_router)
api_router.include_router(attendance_router)
