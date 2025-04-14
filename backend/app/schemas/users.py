from pydantic import BaseModel, EmailStr
from typing import Optional, Literal, List
from datetime import datetime

# User models
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: Optional[Literal["user", "admin"]] = "user"
    ibs_sig: Optional[str] = None
    created_at: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal["user", "admin"]] = None
    password: Optional[str] = None
    ibs_sig: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# TODO: implementar eso en el get users
class UsersList(BaseModel):
    total: int
    users: List[UserInDB]
    page: int
    limit: int
    has_more: bool