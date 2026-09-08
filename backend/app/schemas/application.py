"""
schemas/application.py — Pydantic schemas for job application CRUD.
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, field_validator

from app.models.application import ApplicationStatus, JobType


class ApplicationCreate(BaseModel):
    """Body for POST /api/applications"""
    company: str
    position: str
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: Optional[date] = None
    interview_date: Optional[datetime] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("company")
    @classmethod
    def company_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Company cannot be blank")
        return v.strip()

    @field_validator("position")
    @classmethod
    def position_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Position cannot be blank")
        return v.strip()


class ApplicationUpdate(BaseModel):
    """Body for PUT /api/applications/{id} — all fields optional."""
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    interview_date: Optional[datetime] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    """Full application data returned from the API."""
    id: int
    user_id: int
    company: str
    position: str
    location: Optional[str]
    job_type: Optional[JobType]
    status: ApplicationStatus
    applied_date: Optional[date]
    interview_date: Optional[datetime]
    job_url: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedApplications(BaseModel):
    """Paginated list response with metadata."""
    items: List[ApplicationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
