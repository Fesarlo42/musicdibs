from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import (
    users_router, 
    auth_router, 
    credits_router, 
    genres_router, 
    projects_router, 
    files_router, 
    registration_router,
    conversations_router, 
    messages_router
)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://musicdibs.xyz"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(credits_router, prefix="/api/credits", tags=["credits"])
app.include_router(genres_router, prefix="/api/genres", tags=["genres"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(conversations_router, prefix="/api/conversations", tags=["conversations"])
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
app.include_router(registration_router, prefix="/api/registrations", tags=["registrations"])

@app.get("/api/healthz")
def health_check():
    return {"status": "ok"}

# Serve static files for frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Catch-all: return index.html for all non-API routes
@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}
