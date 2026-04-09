from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from backend.routers import projects, messages, scripts, social_media
from backend.core.database import engine
from backend.models import Base
from backend.exceptions.handlers import get_exception_handlers


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Enable PGVector extension first
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    except Exception as e:
        print(f"Warning: PGVector extension creation failed: {e}")
    
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

# Exception handlers
for exc_type, handler in get_exception_handlers().items():
    app.add_exception_handler(exc_type, handler)
