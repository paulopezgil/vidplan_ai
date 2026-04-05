from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.routers import agent, database
from backend.services.pgvector_service.client import db_client
from backend.services.pgvector_service.ensure_table import ensure_table


@asynccontextmanager
async def lifespan(application: FastAPI):
    await db_client.connect()
    await ensure_table()
    yield
    await db_client.close()


app = FastAPI(title="Vidplan AI", version="0.1.0", lifespan=lifespan)
app.include_router(agent.router)
app.include_router(database.router)
