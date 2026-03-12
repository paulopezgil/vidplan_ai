from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import router as v1_router
from app.services.qdrant_service import ensure_collection


@asynccontextmanager
async def lifespan(application: FastAPI):
    ensure_collection()
    yield


app = FastAPI(title="TalentStream AI", version="0.1.0", lifespan=lifespan)
app.include_router(v1_router)
