from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_db

# pydantic models
from app.schemas import Genre, GenreCreate

# sqlalchemy models
from app.models.models import Genre as GenreModel

router = APIRouter()

@router.get("", response_model=List[Genre])
def get_all_genres(db: Session = Depends(get_db)):
    genres = db.query(GenreModel).all()
    return genres


@router.post("", response_model=Genre, status_code=201)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    # Check if genre with same name already exists
    existing_genre = db.query(GenreModel).filter(GenreModel.name == genre.name).first()
    if existing_genre:
        raise HTTPException(status_code=400, detail="Genre with this name already exists")
    
    # Create new genre
    try:
        db_genre = GenreModel(name=genre.name)
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating new genre: {str(e)}"
        )


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    # Get the genre
    db_genre = db.query(GenreModel).filter(GenreModel.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Delete the genre
    db.delete(db_genre)
    db.commit()
    return None