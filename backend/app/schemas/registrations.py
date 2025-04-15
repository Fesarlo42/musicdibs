from datetime import datetime
from pydantic import BaseModel

# blockhain registration models
class RegistrationBase(BaseModel):
    ibs_id: str


class RegistrationCreate(RegistrationBase):
    pass


class Registration(RegistrationBase):
    id: int
    project_id: int
    registered_at: datetime

    class Config:
        from_attributes = True