"""
models/application.py — SQLAlchemy ORM model for the applications table.

Status and job_type use Python Enums which map to MySQL ENUMs,
giving us controlled values at both the DB and application layer.
"""
import enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Text, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class ApplicationStatus(str, enum.Enum):
    """Controlled status values — prevents arbitrary strings entering the DB."""
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class JobType(str, enum.Enum):
    """Controlled job type values."""
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    REMOTE = "Remote"
    HYBRID = "Hybrid"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key — links each application to exactly one user
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    company: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    job_type: Mapped[Optional[JobType]] = mapped_column(
        Enum(JobType), nullable=True
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED,
        nullable=False,
    )

    applied_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    interview_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    job_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Back-reference to the owning user
    user: Mapped["User"] = relationship("User", back_populates="applications")

    def __repr__(self) -> str:
        return f"<Application id={self.id} company={self.company!r} status={self.status}>"
