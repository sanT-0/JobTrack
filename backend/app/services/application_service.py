"""
services/application_service.py — Business logic for application CRUD.
"""
import math
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus, JobType
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application import ApplicationCreate, ApplicationUpdate, PaginatedApplications, ApplicationResponse


class ApplicationService:

    def __init__(self, db: Session):
        self.repo = ApplicationRepository(db)

    def get_all(
        self,
        user_id: int,
        search: Optional[str] = None,
        status: Optional[ApplicationStatus] = None,
        job_type: Optional[JobType] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedApplications:
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10

        items, total = self.repo.list_paginated(
            user_id=user_id,
            search=search,
            status=status,
            job_type=job_type,
            page=page,
            page_size=page_size,
        )
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return PaginatedApplications(
            items=[ApplicationResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_one(self, application_id: int, user_id: int) -> Application:
        app = self.repo.get_by_id(application_id, user_id)
        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        return app

    def create(self, user_id: int, data: ApplicationCreate) -> Application:
        return self.repo.create(user_id=user_id, **data.model_dump())

    def update(self, application_id: int, user_id: int, data: ApplicationUpdate) -> Application:
        app = self.get_one(application_id, user_id)
        # Only update fields that were explicitly provided (exclude_unset)
        updates = data.model_dump(exclude_unset=True)
        if not updates:
            return app
        return self.repo.update(app, **updates)

    def delete(self, application_id: int, user_id: int) -> None:
        app = self.get_one(application_id, user_id)
        self.repo.delete(app)
