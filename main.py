# main.py — Entry point of the TaskAPI application
#
# This file:
#   1. Creates the FastAPI app instance
#   2. Adds CORS middleware (lets browsers/frontends talk to this API)
#   3. Registers routers (groups of related endpoints)
#   4. Creates all database tables on startup if they don't exist

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, users
from app.database import Base, engine

# Create all database tables defined in models/models.py (safe to call every startup)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskAPI",
    description="A production-ready task management REST API built with FastAPI.",
    version="1.0.0",
)

# Allow any frontend to call this API during development
# In production, replace "*" with your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Each router groups related endpoints together
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/", tags=["Health"])
def health_check():
    """Simple ping endpoint — confirms the API is live."""
    return {"status": "ok", "message": "TaskAPI is running."}
