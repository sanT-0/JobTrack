"""
services/auth_service.py — Business logic for registration, login, and token validation.

Why: Services sit between routes and repositories. They enforce rules like
"email must be unique" and "password must match" without the route needing to know HOW.

How the auth flow works:
  Register: validate → check email unique → hash password → save user → return token
  Login:    find user by email → verify password hash → return token
  Me:       decode JWT → load user from DB → return user data
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.database.connection import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


# FastAPI dependency that extracts the Bearer token from the Authorization header
bearer_scheme = HTTPBearer()


class AuthService:

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> TokenResponse:
        # Check for duplicate email (HTTP 409 Conflict)
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )
        # Hash password — never store plain text
        hashed = hash_password(data.password)
        user = self.repo.create(name=data.name, email=data.email, password_hash=hashed)
        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.repo.get_by_email(data.email)
        # Use the same error for "user not found" and "wrong password"
        # to avoid leaking whether an email exists in the system
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency for protected routes.

    Extracts the Bearer token → decodes it → loads the user from the DB.
    Raises HTTP 401 if the token is missing, invalid, or the user no longer exists.

    Usage in a route:
        def my_route(current_user: User = Depends(get_current_user)):
            ...
    """
    token = credentials.credentials
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repo = UserRepository(db)
    user = repo.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
