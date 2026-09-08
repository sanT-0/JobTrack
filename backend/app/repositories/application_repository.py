"""
repositories/application_repository.py — Data access layer for the applications table.

All queries ensure user_id matches, enforcing data isolation between users.
"""
from datetime import datetime, timezone
from typing import Optional, Tuple, List

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus, JobType


class ApplicationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, application_id: int, user_id: int) -> Optional[Application]:
        """Fetch one application — returns None if it doesn't belong to this user."""
        return (
            self.db.query(Application)
            .filter(Application.id == application_id, Application.user_id == user_id)
            .first()
        )

    def list_paginated(
        self,
        user_id: int,
        search: Optional[str] = None,
        status: Optional[ApplicationStatus] = None,
        job_type: Optional[JobType] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Application], int]:
        """
        Returns a page of applications and the total count.
        Filters are additive (AND logic).
        Search matches company OR position (case-insensitive).
        """
        query = self.db.query(Application).filter(Application.user_id == user_id)

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Application.company.ilike(pattern),
                    Application.position.ilike(pattern),
                    Application.location.ilike(pattern),
                )
            )

        if status:
            query = query.filter(Application.status == status)

        if job_type:
            query = query.filter(Application.job_type == job_type)

        total = query.count()
        items = (
            query
            .order_by(Application.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def create(self, user_id: int, **fields) -> Application:
        app = Application(user_id=user_id, **fields)
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def update(self, application: Application, **fields) -> Application:
        for key, value in fields.items():
            setattr(application, key, value)
        self.db.commit()
        self.db.refresh(application)
        return application

    def delete(self, application: Application) -> None:
        self.db.delete(application)
        self.db.commit()

    # ── Dashboard queries ──────────────────────────────────────

    def count_by_status(self, user_id: int) -> dict:
        """Returns a dict of {status: count} for a user's applications."""
        rows = (
            self.db.query(Application.status, func.count(Application.id))
            .filter(Application.user_id == user_id)
            .group_by(Application.status)
            .all()
        )
        return {row[0].value: row[1] for row in rows}

    def get_total_count(self, user_id: int) -> int:
        return self.db.query(Application).filter(Application.user_id == user_id).count()

    def get_upcoming_interviews(self, user_id: int, limit: int = 10) -> List[Application]:
        """Returns upcoming interviews (interview_date >= now), sorted by date."""
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Application)
            .filter(
                Application.user_id == user_id,
                Application.interview_date >= now,
            )
            .order_by(Application.interview_date.asc())
            .limit(limit)
            .all()
        )
