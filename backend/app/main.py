from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.mongo import init_mongo, close_mongo
from .routers import router as api_router

app = FastAPI(title="Payroll Management API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_mongo(app)


@app.on_event("shutdown")
async def on_shutdown():
    await close_mongo(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(api_router)
