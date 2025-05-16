from fastapi import APIRouter, Response, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Union
import httpx

from app.database import get_db

# pydantic models
from app.schemas import User, UserCreate, UserUpdate, Project, ProjectList, FileResponse, RegistrationResponse

# sqlalchemy models
from app.models import User as UserModel, Project as ProjectModel

# services
from app.services.auth_services import hash_password
from app.services.ibs_services import post_signature, put_signature, get_signature, delete_signature


router = APIRouter()



@router.get("/{user_id}/projects", response_model=ProjectList)
def get_projects(user_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get projects
    all_projects = db.query(ProjectModel).filter(ProjectModel.user_id == user_id)
    total = all_projects.count()

    db_projects = all_projects.order_by(ProjectModel.updated_at.desc()).offset(skip).limit(limit).all()
    
    projects = []
    for db_project in db_projects:
        # Convert files to FileResponse objects
        file_responses = [
            FileResponse(
                id=file.id,
                name=file.name,
                origin=file.origin,
                project_id=file.project_id,
                object_key=file.object_key,
                uploaded_at=file.uploaded_at
            ) 
            for file in db_project.files
        ]
        
        # Get registration if it exists
        registration = None
        if hasattr(db_project, 'registrations') and db_project.registrations:
            reg = db_project.registrations[0]
            registration = RegistrationResponse(
                id=reg.id,
                project_id=reg.project_id,
                ibs_id=reg.ibs_id,
                registered_at=reg.registered_at
            )
        
        # Create Project object with files and registration
        project = Project(
            id=db_project.id,
            name=db_project.name,
            description=db_project.description,
            user_id=db_project.user_id,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at,
            project_genres=db_project.project_genres,
            files=file_responses,
            registration=registration
        )
        projects.append(project)

    return ProjectList(
        total=total,
        projects=projects,
        page=(skip // limit) + 1,
        limit=limit,
        has_more=(skip + limit) < total
    )

@router.post("/{user_id}/signature", status_code=200)
async def make_signature(user_id: int, response: Response, db: Session = Depends(get_db) ):
    # find if the user exists
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.ibs_sig:
        try: 
            sig_data = await get_signature(user.ibs_sig)

            if sig_data["status"] == "success":
                raise HTTPException(status_code=412, detail="Cannot proceed: user already has an active IBS signature.")

            try:
                data = await put_signature(user.ibs_sig)
                return data
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")

        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")

    params = {
        "signature_name": f"{user.id}_{user.first_name}_{user.last_name}"
    }

    try:
        data = await post_signature(params)

        signature_id = data.get("signature_id")

        if not signature_id:
            raise HTTPException(status_code=500, detail="Missing signature_id in response")

        # Update user record
        user.ibs_sig = signature_id
        db.commit()
        db.refresh(user)

        return data
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
    
@router.get("/{user_id}/signature", status_code=200)
async def get_user_signature(user_id: int, response: Response, db: Session = Depends(get_db) ):
    # find if the user exists
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.ibs_sig:
        return {
            "status": "not_found",
            "message": "User does not have an IBS signature."
        }
    
    try: 
        ibs_response = await get_signature(user.ibs_sig)
        return ibs_response

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"External API error: {str(e)}")

@router.get("/{user_id}", response_model=Union[User, str])
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    # find the user by id or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/{user_id}", response_model=Union[User, str])
def update_user(user_id: int, updated_user: UserUpdate, response: Response, db: Session = Depends(get_db)): 
    # find the user by id and update it or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert pydantic model to dict, excluding unset fields
    user_dict = updated_user.dict(exclude_unset=True)
    
    # Handle password hashing
    if "password" in user_dict:
        if not user_dict["password"]:
            del user_dict["password"]
        else:
            user_dict["password"] = hash_password(user_dict["password"])
    
    # Update user attributes
    for key, value in user_dict.items():
        setattr(user, key, value)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)): 
    # find the user by id or 404 if it doesnt exist
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # deletes user ibs signature if there is any
    if user.ibs_sig:
        try:
            await delete_signature(user.ibs_sig)
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting signature from external service: {str(e)}"
            )
        except Exception as e:
            # Handle any other exceptions from the API call
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during signature deletion: {str(e)}"
            )

    try:
        db.delete(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting user: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error deleting user: {str(e)}"
        )

    return Response(status_code = 204)

@router.get("", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("", response_model=User, status_code=201)
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
