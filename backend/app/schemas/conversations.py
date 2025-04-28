from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class ConversationStatus(str, Enum):
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"


class ConversationBase(BaseModel):
    purpose: str
    tempo: str
    key_signature: str
    mood: str
    status: ConversationStatus = ConversationStatus.in_progress


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    purpose: Optional[str] = None
    tempo: Optional[str] = None
    key_signature: Optional[str] = None
    mood: Optional[str] = None
    status: Optional[ConversationStatus] = None


class ConversationResponse(ConversationBase):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True