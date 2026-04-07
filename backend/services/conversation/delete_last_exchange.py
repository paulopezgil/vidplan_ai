from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.services import crud


async def delete_last_exchange(db: AsyncSession, project_id: UUID) -> None:
    """
    Deletes the last user message and any assistant message that follows it.
    """
    
    last_msg = await crud.messages.get_last_project_message(db, project_id)

    # If there are no messages, there's nothing to delete
    if not last_msg:
        return
    
    # Delete all following assistant messages until we hit a user message
    if last_msg.role == "assistant":
        # Delete the assistant message first
        await crud.messages.delete_message(db, last_msg)
        
        # Now delete the user message before it
        await delete_last_exchange(db, project_id)  # Recursive call to handle the next message
    
    # If the last message is a user message, delete it
    elif last_msg.role == "user":
        await crud.messages.delete_message(db, last_msg)

    # If we encounter an unexpected role, we ignore it and stop the deletion process