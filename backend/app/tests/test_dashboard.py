"""
tests/test_dashboard.py — Tests for dashboard statistics and upcoming interviews.
"""
from datetime import datetime, timezone, timedelta
from app.tests.conftest import register_user, get_auth_headers


APP_BASE = {
    "company": "Test Co",
    "position": "Dev",
    "status": "Applied",
}


class TestDashboardStats:

    def test_stats_empty(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.get("/api/dashboard/stats", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["applied"] == 0
        assert data["interview"] == 0

    def test_stats_counts_correctly(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        statuses = ["Applied", "Applied", "Interview", "Offer", "Rejected"]
        for s in statuses:
            client.post("/api/applications", json={**APP_BASE, "status": s}, headers=headers)

        resp = client.get("/api/dashboard/stats", headers=headers)
        data = resp.json()
        assert data["total"] == 5
        assert data["applied"] == 2
        assert data["interview"] == 1
        assert data["offer"] == 1
        assert data["rejected"] == 1
        assert data["shortlisted"] == 0

    def test_stats_requires_auth(self, client):
        resp = client.get("/api/dashboard/stats")
        assert resp.status_code in (401, 403)

    def test_stats_isolated_between_users(self, client):
        """User B's stats should not include User A's applications."""
        register_user(client, email="user_a@example.com")
        register_user(client, name="User B", email="user_b@example.com")
        headers_a = get_auth_headers(client, email="user_a@example.com")
        headers_b = get_auth_headers(client, email="user_b@example.com")

        client.post("/api/applications", json={**APP_BASE, "status": "Offer"}, headers=headers_a)
        resp = client.get("/api/dashboard/stats", headers=headers_b)
        assert resp.json()["total"] == 0


class TestUpcomingInterviews:

    def test_upcoming_interviews_empty(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.get("/api/dashboard/upcoming-interviews", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_upcoming_interviews_returns_future_only(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        future = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
        past = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()

        client.post("/api/applications", json={
            **APP_BASE, "status": "Interview", "interview_date": future
        }, headers=headers)
        client.post("/api/applications", json={
            **APP_BASE, "status": "Interview", "interview_date": past
        }, headers=headers)

        resp = client.get("/api/dashboard/upcoming-interviews", headers=headers)
        data = resp.json()
        assert len(data) == 1  # Only the future interview

    def test_upcoming_interviews_sorted_by_date(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        d1 = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
        d2 = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
        d3 = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()

        for d in [d1, d2, d3]:
            client.post("/api/applications", json={
                **APP_BASE, "status": "Interview", "interview_date": d
            }, headers=headers)

        resp = client.get("/api/dashboard/upcoming-interviews", headers=headers)
        dates = [item["interview_date"] for item in resp.json()]
        assert dates == sorted(dates)
