from pydantic import BaseModel, EmailStr

# User authentication models
class UserLogin(BaseModel):
    email: EmailStr
    password: str