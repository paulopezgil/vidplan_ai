from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.services.crud.scripts import get_project_script, create_script, update_script
from backend.schemas.script import ScriptUpdate

async def update_tab(db: AsyncSession, project_id: UUID, content: str) -> str:
    """Updates or creates the script content in the database (Script Tab)."""
    script = await get_project_script(db, project_id)
    
    if script:
        update_data = ScriptUpdate(content=content)
        await update_script(db, script, update_data)
    else:
        await create_script(db, project_id, content)
        
    return "Script Tab updated successfully."
