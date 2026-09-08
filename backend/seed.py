"""
seed.py — Development seed script.

Creates one demo user with realistic job applications in various statuses,
including two upcoming interviews.

Usage:
    cd backend
    python seed.py

DO NOT run in production.
"""
import sys
import os
from datetime import datetime, timedelta, date, timezone

# Allow running from the backend/ directory
sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal, engine, Base
from app.models import user, application  # registers models with Base
from app.core.security import hash_password
from app.models.user import User
from app.models.application import Application, ApplicationStatus, JobType


def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Clean existing demo user to allow re-running safely
        existing = db.query(User).filter(User.email == "demo@jobtrack.dev").first()
        if existing:
            db.delete(existing)
            db.commit()
            print("Removed existing demo user.")

        # Create demo user
        demo_user = User(
            name="Alex Johnson",
            email="demo@jobtrack.dev",
            password_hash=hash_password("demo1234"),
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print(f"Created demo user: demo@jobtrack.dev / demo1234")

        now = datetime.now(timezone.utc)
        today = date.today()

        apps = [
            Application(
                user_id=demo_user.id,
                company="Google",
                position="Software Engineer II",
                location="Mountain View, CA",
                job_type=JobType.FULL_TIME,
                status=ApplicationStatus.INTERVIEW,
                applied_date=today - timedelta(days=20),
                interview_date=now + timedelta(days=3),
                job_url="https://careers.google.com",
                notes="Technical interview round 2. Review system design.",
            ),
            Application(
                user_id=demo_user.id,
                company="Stripe",
                position="Backend Engineer",
                location="Remote",
                job_type=JobType.REMOTE,
                status=ApplicationStatus.INTERVIEW,
                applied_date=today - timedelta(days=14),
                interview_date=now + timedelta(days=7),
                job_url="https://stripe.com/jobs",
                notes="First interview with hiring manager scheduled.",
            ),
            Application(
                user_id=demo_user.id,
                company="Meta",
                position="Python Developer",
                location="Menlo Park, CA",
                job_type=JobType.FULL_TIME,
                status=ApplicationStatus.SHORTLISTED,
                applied_date=today - timedelta(days=10),
                job_url="https://metacareers.com",
                notes="Passed initial screening, waiting for technical round.",
            ),
            Application(
                user_id=demo_user.id,
                company="Spotify",
                position="Full-Stack Developer",
                location="New York, NY",
                job_type=JobType.HYBRID,
                status=ApplicationStatus.APPLIED,
                applied_date=today - timedelta(days=5),
                job_url="https://spotify.com/jobs",
                notes="Applied via LinkedIn. Follow up in a week.",
            ),
            Application(
                user_id=demo_user.id,
                company="Airbnb",
                position="React Developer",
                location="San Francisco, CA",
                job_type=JobType.FULL_TIME,
                status=ApplicationStatus.APPLIED,
                applied_date=today - timedelta(days=3),
                job_url="https://careers.airbnb.com",
                notes="",
            ),
            Application(
                user_id=demo_user.id,
                company="Amazon",
                position="Software Development Engineer",
                location="Seattle, WA",
                job_type=JobType.FULL_TIME,
                status=ApplicationStatus.REJECTED,
                applied_date=today - timedelta(days=30),
                notes="Rejected after online assessment. Study DP problems.",
            ),
            Application(
                user_id=demo_user.id,
                company="Shopify",
                position="Python Backend Developer",
                location="Remote",
                job_type=JobType.REMOTE,
                status=ApplicationStatus.OFFER,
                applied_date=today - timedelta(days=45),
                notes="Offer received! $130k + equity. Deadline to decide: next Friday.",
            ),
            Application(
                user_id=demo_user.id,
                company="Netflix",
                position="Senior Software Engineer",
                location="Los Gatos, CA",
                job_type=JobType.FULL_TIME,
                status=ApplicationStatus.WITHDRAWN,
                applied_date=today - timedelta(days=25),
                notes="Withdrew — accepted another offer.",
            ),
            Application(
                user_id=demo_user.id,
                company="Notion",
                position="Full-Stack Engineer",
                location="San Francisco, CA",
                job_type=JobType.HYBRID,
                status=ApplicationStatus.APPLIED,
                applied_date=today - timedelta(days=1),
                job_url="https://notion.so/jobs",
            ),
            Application(
                user_id=demo_user.id,
                company="Linear",
                position="Frontend Engineer",
                location="Remote",
                job_type=JobType.REMOTE,
                status=ApplicationStatus.SHORTLISTED,
                applied_date=today - timedelta(days=8),
                job_url="https://linear.app/jobs",
                notes="Contacted by recruiter after applying.",
            ),
        ]

        db.add_all(apps)
        db.commit()
        print(f"Created {len(apps)} demo applications.")
        print("\n[SUCCESS] Seed complete!")
        print("   Login: demo@jobtrack.dev")
        print("   Password: demo1234")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
