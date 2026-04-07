from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.services.crud.projects import get_project, update_project
from backend.schemas.project import ProjectUpdate

async def update_tab(db: AsyncSession, project_id: UUID, title: str, description: str) -> str:
    """Updates the project title and description in the database (Project Tab)."""
    project = await get_project(db, project_id)
    if not project:
        return "Failed to find project."
    
    update_data = ProjectUpdate(title=title, description=description)
    await update_project(db, project, update_data)
    return "Project Tab updated successfully."
