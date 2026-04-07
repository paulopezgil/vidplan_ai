from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.routers import projects, messages, scripts, social_media
from backend.core.database import engine
from backend.models import Base


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Create database tables (in production, use migrations instead)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Warning: Database table creation failed: {e}")
    yield
    # Cleanup if needed
    try:
        await engine.dispose()
    except Exception:
        pass


app = FastAPI(title="Vidplan AI", version="0.1.0", lifespan=lifespan)

# Data Routes
app.include_router(projects.router)
app.include_router(messages.router)
app.include_router(scripts.router)
app.include_router(social_media.router)
