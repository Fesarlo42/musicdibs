# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

# pydantic models
from app.schemas import UserLogin, Token

# sqlalchemy models
from app.models.models import User

# services
from app.services.auth_services import verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user_id": user.id, 
        "role": user.role
    }

@router.get("/me", response_model=dict, include_in_schema=False)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/has-permission")
async def check_permission(
    necessary_role: str, 
    current_user: dict = Depends(get_current_user)
):
    user_role = current_user.get("role")
    
    if user_role != necessary_role:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
    
    return {"has_permission": True}