"""
schemas/auth.py — Pydantic schemas for authentication request/response bodies.

Why: Schemas define what data flows in/out of endpoints.
They validate input automatically and shape API responses.
Passwords are write-only — they never appear in response models.
"""
from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    """Body for POST /api/auth/register"""
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    """Body for POST /api/auth/login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response from login/register — contains the JWT."""
    access_token: str
    token_type: str = "bearer"
