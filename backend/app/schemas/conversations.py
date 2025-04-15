from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from .messages import Message

# conversations models
class ConversationBase(BaseModel):
    title: str
    purpose: str
    tempo: str
    key_signature: str
    mood: str
    status: str = "in_progress"


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    purpose: Optional[str] = None
    tempo: Optional[str] = None
    key_signature: Optional[str] = None
    mood: Optional[str] = None
    status: Optional[str] = None


class Conversation(ConversationBase):
    id: int
    project_id: int
    created_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True
