from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from .project_genres import ProjectGenre
from .files import FileResponse
from .conversations import Conversation
from .registrations import Registration

# projects models
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int


class ProjectCreate(ProjectBase):
    project_genres: Optional[List[int]] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_genres: List[ProjectGenre] = []
    files: List[FileResponse] = []
    conversations: List[Conversation] = []
    registrations: List[Registration] = []

    class Config:
        from_attributes = True


class ProjectResponse(Project):
    pass


class ProjectList(BaseModel):
    projects: List[Project]
    total: int
    page: int
    limit: int
    has_more: bool