import os
from typing import Optional

from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv


MONGO_URI_ENV = "MONGODB_URI"
DB_NAME_ENV = "MONGODB_DB_NAME"
load_dotenv()


async def init_mongo(app: FastAPI) -> None:
    uri = os.getenv(MONGO_URI_ENV)
    if not uri:
        raise RuntimeError(f"Environment variable {MONGO_URI_ENV} is not set.")
    db_name = os.getenv(DB_NAME_ENV, "payroll")
    client = MongoClient(uri)
    app.state.mongo_client = client
    app.state.db = client[db_name]


async def close_mongo(app: FastAPI) -> None:
    client: Optional[MongoClient] = getattr(app.state, "mongo_client", None)
    if client:
        client.close()
