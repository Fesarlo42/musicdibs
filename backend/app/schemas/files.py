from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    name: str
    origin: str = "user_upload"

class FileCreate(FileBase):
    project_id: int

class FileResponse(FileBase):
    id: int
    project_id: int
    object_key: str
    uploaded_at: datetime
    
    class Config:
        from_attribute = True