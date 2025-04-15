from datetime import datetime
from pydantic import BaseModel

class MessageBase(BaseModel):
    is_from_ai: bool
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    conversation_id: int
    sent_at: datetime

    class Config:
        from_attribute = True