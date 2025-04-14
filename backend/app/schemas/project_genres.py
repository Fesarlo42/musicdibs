from pydantic import BaseModel

from .genres import Genre

class ProjectGenreCreate(BaseModel):
    genre_id: int


class ProjectGenre(BaseModel):
    genre: Genre

    class Config:
        from_attributes = True