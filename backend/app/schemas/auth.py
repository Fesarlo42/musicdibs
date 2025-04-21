from pydantic import BaseModel, EmailStr

# User authentication models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str