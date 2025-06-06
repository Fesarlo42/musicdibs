from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from .project_genres import ProjectGenre
from .files import FileResponse
from .registrations import RegistrationResponse

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
    registration: Optional[RegistrationResponse] = None

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

class ProjectStats(BaseModel):
    total_projects: int
    total_registrations: int
    total_conversations: int