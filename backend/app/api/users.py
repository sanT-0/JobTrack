"""
api/users.py — User profile endpoints.

GET /api/users/me  — View profile
PUT /api/users/me  — Update name, email, or password
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.database.connection import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UpdateProfileRequest
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
def update_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update name, email, or password.
    - Changing email: checks uniqueness.
    - Changing password: requires current_password for verification.
    """
    repo = UserRepository(db)
    updates = {}

    if data.name is not None:
        updates["name"] = data.name

    if data.email is not None and data.email != current_user.email:
        # Make sure the new email is not already taken
        existing = repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already in use",
            )
        updates["email"] = data.email

    if data.new_password is not None:
        if not data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="current_password is required to set a new password",
            )
        if not verify_password(data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect",
            )
        updates["password_hash"] = hash_password(data.new_password)

    if not updates:
        return current_user

    return repo.update(current_user, **updates)
