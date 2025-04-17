from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class RegistrationBase(BaseModel):
    project_id: int

class RegistrationCreate(RegistrationBase):
    title: str

class RegistrationResponse(RegistrationBase):
    id: int
    ibs_id: str
    registered_at: datetime
    
    class Config:
        from_attributes = True

class RegistrationDetailResponse(RegistrationResponse):
    evidence_details: Dict[str, Any]