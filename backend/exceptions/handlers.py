import os
from typing import Any

from backend.schemas.error import ErrorResponse
from backend.exceptions.base import (
    VidPlanError,
    NotFoundError,
    AgentError,
    DatabaseError,
    ValidationError,
    UnauthorizedError,
)

DEV_MODE = os.getenv("ENV", "production") == "development"


async def handle_vidplan_exception(exc: VidPlanError, status_code: int = None, error_code: str = None) -> ErrorResponse:
    status_code = status_code or 500
    error_code = error_code or exc.__class__.__name__.replace("Error", "").upper()
    detail = exc.detail if DEV_MODE else None
    
    return ErrorResponse(
        status_code=status_code,
        content=ErrorResponse(
            error_code=error_code,
            message=exc.message,
            detail=detail,
        ).model_dump(exclude_none=True),
    )


async def handle_not_found_error(exc: NotFoundError) -> ErrorResponse:
    return await handle_vidplan_exception(exc, status_code=404, error_code="NOT_FOUND")


async def handle_agent_error(exc: AgentError) -> ErrorResponse:
    return await handle_vidplan_exception(exc, status_code=500, error_code="AGENT_ERROR")


async def handle_database_error(exc: DatabaseError) -> ErrorResponse:
    return await handle_vidplan_exception(exc, status_code=500, error_code="DATABASE_ERROR")


async def handle_validation_error(exc: ValidationError) -> ErrorResponse:
    return await handle_vidplan_exception(exc, status_code=400, error_code="VALIDATION_ERROR")


async def handle_unauthorized_error(exc: UnauthorizedError) -> ErrorResponse:
    return await handle_vidplan_exception(exc, status_code=401, error_code="UNAUTHORIZED")