"""
api/applications.py — Application CRUD endpoints.

All endpoints require authentication (current_user dependency).
All queries are scoped to current_user.id, so users can only touch their own data.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.application import ApplicationStatus, JobType
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    PaginatedApplications,
)
from app.services.application_service import ApplicationService
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.get(
    "",
    response_model=PaginatedApplications,
    summary="List applications with search, filter, and pagination",
)
def list_applications(
    search: Optional[str] = Query(None, description="Search company, position, or location"),
    status: Optional[ApplicationStatus] = Query(None, description="Filter by status"),
    job_type: Optional[JobType] = Query(None, description="Filter by job type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.get_all(
        user_id=current_user.id,
        search=search,
        status=status,
        job_type=job_type,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Get a single application by ID",
)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.get_one(application_id, current_user.id)


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=201,
    summary="Create a new job application",
)
def create_application(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.create(current_user.id, data)


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Update an existing application",
)
def update_application(
    application_id: int,
    data: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.update(application_id, current_user.id, data)


@router.delete(
    "/{application_id}",
    status_code=204,
    summary="Delete an application",
)
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    service.delete(application_id, current_user.id)
