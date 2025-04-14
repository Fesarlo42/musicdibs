from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_db

# pydantic models
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse

# sqlalchemy models
from app.models import Project as ProjectModel, ProjectGenre as ProjectGenreModel, Genre as GenreModel


router = APIRouter()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    return db_project

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        # Create the project first without genres
        db_project = ProjectModel(
            name=project.name,
            description=project.description,
            user_id=project.user_id
        )
        
        db.add(db_project)
        db.flush()  # This assigns an ID to db_project but doesn't commit yet
        
        # Now create the project_genre relationships
        for genre_id in project.project_genres:
            db_project_genre = ProjectGenreModel(
                project_id=db_project.id,
                genre_id=genre_id
            )
            db.add(db_project_genre)
        
        db.commit()
        db.refresh(db_project)
        
        return db_project

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating project: {str(e)}"
        )


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, updated_project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    update_data = updated_project.dict(exclude_unset=True)
    
    # Handle project_genres separately if it exists in the update data
    if "project_genres" in update_data:
        genre_ids = update_data.pop("project_genres")  # Remove from update_data to handle separately
        
        # Delete existing genre relationships
        db.query(ProjectGenreModel).filter(ProjectGenreModel.project_id == project_id).delete()
        
        # Create new genre relationships
        for genre_id in genre_ids:
            db_project_genre = ProjectGenreModel(
                project_id=project_id,
                genre_id=genre_id
            )
            db.add(db_project_genre)
    
    # Update regular fields
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    try:
        db.commit()
        db.refresh(db_project)
        return db_project

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error updating project: {str(e)}"
        )

@router.delete("/{project_id}")
def delete_project(project_id: int,  response: Response, db: Session = Depends(get_db)):
    # find the project by id or 404 if it doesnt exist
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    try:
        db.delete(project)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting project: {str(e)}"
        )

    return Response(status_code = 200)


# Genre related endpoints

@router.post("/{project_id}/genres/{genre_id}", status_code=201)
def add_genre_to_project(
    project_id: int, 
    genre_id: int,  # Could also accept this as a body parameter
    db: Session = Depends(get_db)
):
    # Verify the project exists
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verify the genre exists
    db_genre = db.query(GenreModel).filter(GenreModel.id == genre_id).first()
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Check if relationship already exists
    existing = db.query(ProjectGenreModel).filter(
        ProjectGenreModel.project_id == project_id,
        ProjectGenreModel.genre_id == genre_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="This genre is already in the project")
    
    # Create the relationship
    db_project_genre = ProjectGenreModel(project_id=project_id, genre_id=genre_id)
    db.add(db_project_genre)
    db.commit()
    
    return {"message": "Genre added to project successfully"}


@router.delete("/{project_id}/genres/{genre_id}")
def remove_genre_from_project(
    project_id: int, 
    genre_id: int,
    response: Response,
    db: Session = Depends(get_db)
):
    # Find the relationship
    db_project_genre = db.query(ProjectGenreModel).filter(
        ProjectGenreModel.project_id == project_id,
        ProjectGenreModel.genre_id == genre_id
    ).first()
    
    if not db_project_genre:
        raise HTTPException(status_code=404, detail="Genre not found in this project")
    
    # Delete the relationship
    db.delete(db_project_genre)
    db.commit()
    
    return Response(status_code = 200)  # 204 No Content response