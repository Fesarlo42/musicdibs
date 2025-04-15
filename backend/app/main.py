from fastapi import FastAPI
from app.routes import users_router, auth_router, credits_router, genres_router, projects_router, files_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(credits_router, prefix="/credits", tags=["credits"])
app.include_router(genres_router, prefix="/genres", tags=["genres"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(files_router, prefix="/files", tags=["files"])
