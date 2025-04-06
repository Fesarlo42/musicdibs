from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union

from app.database import get_db

# pydantic models
from app.schemas import User, UserCreate, UserUpdate

# sqlalchemy models
from app.models import User as UserModel

# utils
from app.utils.auth import hash_password

router = APIRouter()

@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/{user_id}", response_model=Union[User, str])
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    # find the user by id or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Convert Pydantic UserCreate to SQLAlchemy UserModel
    try:
        db_user = UserModel(
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            password=hash_password(user.password),
            role = user.role,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return User.from_orm(db_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating new user: {str(e)}"
        )

@router.put("/{user_id}", response_model=Union[User, str])
def update_user(user_id: int, updated_user: UserUpdate, response: Response, db: Session = Depends(get_db)): 
    # find the user by id and update it or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = updated_user.dict(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)): 
    # find the user by id and update it or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()

    return Response(status_code = 200)
