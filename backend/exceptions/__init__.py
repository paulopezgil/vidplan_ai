"""
VidPlan AI Exceptions Module.

Exports all exceptions and handlers for use throughout the application.

Example usage:
    from backend.exceptions import ProjectNotFoundError
    from backend.exceptions.handlers import register_exception_handlers
"""

# Base HTTP exceptions
from backend.exceptions.base import (
    AppError,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    DatabaseError,
    ExternalServiceError,
    RateLimitError,
)

# Domain-specific exceptions
from backend.exceptions.project import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectCreationError,
)

from backend.exceptions.message import (
    MessageNotFoundError,
    NoMessagesError,
)

from backend.exceptions.script import (
    ScriptNotFoundError,
    ScriptValidationError,
)

from backend.exceptions.social_media import (
    SocialMediaNotFoundError,
    SocialMediaValidationError,
)

from backend.exceptions.agent import (
    AgentResponseError,
    AgentOverloadedError,
)

# Handlers
from backend.exceptions.handlers import (
    register_exception_handlers,
)

__all__ = [
    # Base HTTP exceptions
    "AppError",
    "NotFoundError",
    "ValidationError",
    "UnauthorizedError",
    "DatabaseError",
    "ExternalServiceError",
    "RateLimitError",
    # Project exceptions
    "ProjectNotFoundError",
    "ProjectValidationError",
    "ProjectCreationError",
    # Message exceptions
    "MessageNotFoundError",
    "NoMessagesError",
    # Script exceptions
    "ScriptNotFoundError",
    "ScriptValidationError",
    # Social media exceptions
    "SocialMediaNotFoundError",
    "SocialMediaValidationError",
    # Agent exceptions
    "AgentResponseError",
    "AgentOverloadedError",
    # Handlers
    "register_exception_handlers",
]
