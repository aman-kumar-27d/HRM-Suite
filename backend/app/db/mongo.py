import os
from typing import Optional

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


MONGO_URI_ENV = "MONGODB_URI"
DB_NAME_ENV = "MONGODB_DB_NAME"

# Load environment from .env if present
load_dotenv()


async def init_mongo(app: FastAPI) -> None:
    uri = os.getenv(MONGO_URI_ENV)
    if not uri:
        raise RuntimeError(
            f"Environment variable {MONGO_URI_ENV} is not set. Configure MongoDB URI in .env."
        )
    db_name = os.getenv(DB_NAME_ENV, "payroll")
    client = AsyncIOMotorClient(uri)
    app.state.mongo_client = client
    app.state.db = client[db_name]


async def close_mongo(app: FastAPI) -> None:
    client: Optional[AsyncIOMotorClient] = getattr(app.state, "mongo_client", None)
    if client:
        client.close()
