from typing import List, Any, Dict
from pydantic import BaseModel

from grinning_cat_python_sdk.models.api.nested.memories import ConversationMessage


class ConversationDeleteOutput(BaseModel):
    deleted: bool


class ConversationHistoryOutput(BaseModel):
    history: List[ConversationMessage]


class ConversationsResponse(BaseModel):
    chat_id: str
    name: str
    num_messages: int
    metadata: Dict[str, Any]
    created_at: float | None
    updated_at: float | None


class ConversationAttributesChangeOutput(BaseModel):
    changed: bool