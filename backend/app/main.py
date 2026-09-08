"""
main.py — FastAPI application entry point.

This file:
  1. Creates the FastAPI app with metadata for Swagger docs
  2. Configures CORS so the React frontend can talk to the API
  3. Creates all database tables on startup
  4. Registers all API routers
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import engine, Base

# Import all models so SQLAlchemy knows about them before create_all
from app.models import user, application  # noqa: F401

# Import routers
from app.api import auth, applications, dashboard, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup if database is accessible."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[JobTrack] Database initialization warning: {e}")
    yield


# ── App definition ────────────────────────────────────────────────────────────
app = FastAPI(
    title="JobTrack API",
    description=(
        "REST API for the JobTrack Job Application & Interview Management System.\n\n"
        "## Authentication\n"
        "Most endpoints require a `Bearer` JWT token in the `Authorization` header.\n"
        "Get a token from `POST /api/auth/login` or `POST /api/auth/register`."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows the React dev server (port 5173) and production frontend to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(dashboard.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — returns API status."""
    return {"status": "ok", "message": "JobTrack API is running", "docs": "/docs"}
