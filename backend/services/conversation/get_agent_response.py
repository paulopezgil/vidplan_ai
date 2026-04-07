from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.message import Message
from backend.services import crud
from backend.services.agent import generate_agent_response


async def get_agent_response(db: AsyncSession, project_id: UUID, content: str) -> Message:
    """
    Gets an AI response for a user message following single responsibility principle.
    """
    # 1. Fetch last 10 messages for context
    history = await crud.messages.get_last_project_messages(db, project_id, 10)
    
    # 2. Persist User Message
    await crud.messages.create_message(db, project_id, "user", content)
    
    # 3. Get AI Response (Passing history explicitly)
    ai_text = await generate_agent_response(db, project_id, content, history)
    
    # 4. Persist and return AI Message
    return await crud.messages.create_message(db, project_id, "assistant", ai_text)
