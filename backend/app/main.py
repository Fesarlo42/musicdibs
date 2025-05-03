from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users_router, auth_router, credits_router, genres_router, projects_router, files_router, registration_router, conversations_router, messages_router

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",  # frontend
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(credits_router, prefix="/credits", tags=["credits"])
app.include_router(genres_router, prefix="/genres", tags=["genres"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(files_router, prefix="/files", tags=["files"])
app.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
app.include_router(messages_router, prefix="/messages", tags=["messages"])
app.include_router(registration_router, prefix="/registrations", tags=["registrations"])
