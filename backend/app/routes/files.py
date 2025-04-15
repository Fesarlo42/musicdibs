from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import io

from app.database import get_db
from app.services.files_services import upload_file, delete_file, get_presigned_url

# pydantic models
from app.schemas import FileResponse

# sqlalchemy models
from app.models.models import File as FileModel, Project as ProjectModel

router = APIRouter()

@router.post("/{project_id}", response_model=FileResponse, status_code=201)
async def upload_project_file(
    project_id: int,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):

    # Verify project exists
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Upload file to MinIO
    try:
        object_key = upload_file(file)
        
        # Save file record to database
        db_file = FileModel(
            project_id=project_id,
            object_key=object_key,
            name=file.filename,
            origin="user_upload"
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return db_file
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.delete("/{file_id}", status_code=204)
async def delete_project_file(
    file_id: int,
    db: Session = Depends(get_db)
):
      
    # Find the file record
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=404,
            detail=f"File with ID {file_id} not found"
        )
    
    try:
        # Delete from MinIO storage
        delete_file(db_file.object_key)
        
        # Delete from database
        db.delete(db_file)
        db.commit()
        
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {str(e)}"
        )


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    
    # Find the file record
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=404,
            detail=f"File with ID {file_id} not found"
        )
    
    try:
        # Generate presigned URL
        presigned_url = get_presigned_url(db_file.object_key)
        
        # Return URL for frontend to use
        return {"download_url": presigned_url, "filename": db_file.name}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate download link: {str(e)}"
        )


@router.get("/project/{project_id}", response_model=List[FileResponse])
async def get_project_files(
    project_id: int,
    db: Session = Depends(get_db)
):
    
    # Verify project exists
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    files = db.query(FileModel).filter(FileModel.project_id == project_id).all()
    return files