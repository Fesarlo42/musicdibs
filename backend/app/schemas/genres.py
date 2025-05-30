from pydantic import BaseModel

# Genres models
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    
    class Config:
        from_attributes = True
