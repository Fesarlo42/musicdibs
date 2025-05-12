from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db

# pydantic models
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStats, RegistrationResponse, ConversationCreate, ConversationUpdate, ConversationResponse

# sqlalchemy models
from app.models import Project as ProjectModel, ProjectGenre as ProjectGenreModel, Genre as GenreModel, Conversation as ConversationModel, Registration as RegistrationModel


router = APIRouter()

# Genre related endpoints
@router.post("/{project_id}/genres/{genre_id}", status_code=201)
def add_genre_to_project(
    project_id: int, 
    genre_id: int,
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
    
    return Response(status_code = 200)


# Conversation related endpoints
@router.get("/{project_id}/conversation", response_model=ConversationResponse)
def get_conversation(project_id: int, db: Session = Depends(get_db)):
    # Verify the project exists
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    
    # Get the conversation for this project
    conversation = db.query(ConversationModel).filter(
        ConversationModel.project_id == project_id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail=f"No conversation found for project {project_id}"
        )
    
    return conversation


# Stats
@router.get("/stats", response_model=ProjectStats)
def get_project_stats(db: Session = Depends(get_db)):
    try:
        total_projects = db.query(ProjectModel).count()
        total_registrations = db.query(RegistrationModel).count()
        total_conversations = db.query(ConversationModel).count()
        
        print(f"Debug values: projects={total_projects}, registrations={total_registrations}, conversations={total_conversations}")
        
        return ProjectStats(
            total_projects=total_projects,
            total_registrations=total_registrations,
            total_conversations=total_conversations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# Project related endpoints
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Get registration data if it exists
    registration = None
    if hasattr(db_project, 'registrations') and db_project.registrations:
        reg = db_project.registrations[0]
        registration = RegistrationResponse(
            id=reg.id,
            project_id=reg.project_id,
            ibs_id=reg.ibs_id,
            registered_at=reg.registered_at
        )
    
    # Create a ProjectResponse with the registration included
    response_data = {}

    # Loop through all attributes in the db_project model
    for key, value in db_project.__dict__.items():
        if not key.startswith('_'):
            response_data[key] = value

     # Add relationship collections explicitly
    if hasattr(db_project, 'files'):
        response_data['files'] = db_project.files
    
    if hasattr(db_project, 'project_genres'):
        response_data['project_genres'] = db_project.project_genres
    
    response_data['registration'] = registration
    
    return response_data

@router.post("", response_model=ProjectResponse, status_code=201)
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

@router.delete("/{project_id}", status_code=204)
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
