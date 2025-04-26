# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db

# pydantic models
from app.schemas import User

# sqlalchemy models
from app.models.models import User as UserModel

# services
from app.services.auth_services import verify_password

router = APIRouter()

@router.post("/login", response_model=User)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print('form data:')
    print(form_data.username, form_data.password)
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Just return the user data
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "ibs_sig": user.ibs_sig,
        "created_at": user.created_at
    }

@router.get("/{user_id}/has-permission", status_code=200)
async def check_permission(
    user_id: int, role: str, db: Session = Depends(get_db)
):
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role != role:
        return {"has_permission": False}
    
    return {"has_permission": True}