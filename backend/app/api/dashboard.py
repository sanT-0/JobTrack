"""
api/dashboard.py — Dashboard statistics endpoints.

GET /api/dashboard/stats             — Status counts for current user
GET /api/dashboard/upcoming-interviews — Next upcoming interviews
"""
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application import ApplicationResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


class DashboardStats(BaseModel):
    total: int
    applied: int
    shortlisted: int
    interview: int
    offer: int
    rejected: int
    withdrawn: int


@router.get(
    "/stats",
    response_model=DashboardStats,
    summary="Get application status counts for the dashboard",
)
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns a count for each application status plus the total."""
    repo = ApplicationRepository(db)
    counts = repo.count_by_status(current_user.id)
    total = repo.get_total_count(current_user.id)
    return DashboardStats(
        total=total,
        applied=counts.get("Applied", 0),
        shortlisted=counts.get("Shortlisted", 0),
        interview=counts.get("Interview", 0),
        offer=counts.get("Offer", 0),
        rejected=counts.get("Rejected", 0),
        withdrawn=counts.get("Withdrawn", 0),
    )


@router.get(
    "/upcoming-interviews",
    response_model=List[ApplicationResponse],
    summary="Get upcoming interviews sorted by date",
)
def get_upcoming_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns interviews with a future interview_date, sorted ascending."""
    repo = ApplicationRepository(db)
    return repo.get_upcoming_interviews(current_user.id)
