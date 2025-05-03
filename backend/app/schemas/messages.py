from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    content: str
    is_from_ai: bool

class MessageCreate(MessageBase):
    conversation_id: int

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sent_at: datetime
    
    class Config:
        from_attributes = True

class MessageGenerateRequest(BaseModel):
    conversation_id: int
    user_message: str
    content_type: Optional[str] = "lyrics"