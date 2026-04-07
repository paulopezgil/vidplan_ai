from typing import List
from backend.models.message import Message
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart

def build_message_history(db_messages: List[Message]) -> list[ModelMessage]:
    """Convert DB messages to Pydantic AI ModelMessage history."""
    history = []
    for msg in db_messages:
        if msg.role == "user":
            history.append(ModelRequest(parts=[TextPart(content=msg.content)]))
        elif msg.role == "assistant":
            history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return history
