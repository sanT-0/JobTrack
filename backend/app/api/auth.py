"""
api/auth.py — Authentication endpoints.

POST /api/auth/register  — Create account, returns JWT
POST /api/auth/login     — Verify credentials, returns JWT
GET  /api/auth/me        — Returns current user (protected)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Register a new user account",
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - Validates name, email format, and password length (≥8 chars)
    - Returns a JWT access token on success
    - Returns 409 if email already exists
    """
    service = AuthService(db)
    return service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    - Returns 401 for invalid credentials (same message for unknown email
      and wrong password to avoid user enumeration)
    """
    service = AuthService(db)
    return service.login(data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
)
def me(current_user: User = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    Requires a valid Bearer token in the Authorization header.
    """
    return current_user
