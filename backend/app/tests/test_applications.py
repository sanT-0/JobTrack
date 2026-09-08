"""
tests/test_applications.py — Tests for application CRUD, authorization, search, filtering.
"""
import pytest
from app.tests.conftest import register_user, get_auth_headers

APP_PAYLOAD = {
    "company": "Acme Corp",
    "position": "Software Engineer",
    "location": "New York",
    "job_type": "Full-Time",
    "status": "Applied",
}


def create_app(client, headers, payload=None):
    """Helper: create an application and return the response."""
    return client.post("/api/applications", json=payload or APP_PAYLOAD, headers=headers)


class TestCreateApplication:

    def test_create_success(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = create_app(client, headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["company"] == "Acme Corp"
        assert data["position"] == "Software Engineer"
        assert data["status"] == "Applied"

    def test_create_requires_auth(self, client):
        resp = client.post("/api/applications", json=APP_PAYLOAD)
        assert resp.status_code in (401, 403)

    def test_create_missing_company(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.post("/api/applications", json={"position": "Dev"}, headers=headers)
        assert resp.status_code == 422

    def test_create_invalid_status(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.post("/api/applications", json={**APP_PAYLOAD, "status": "Banana"}, headers=headers)
        assert resp.status_code == 422


class TestGetApplications:

    def test_list_own_applications(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        create_app(client, headers)
        create_app(client, headers, {**APP_PAYLOAD, "company": "Beta Inc"})
        resp = client.get("/api/applications", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_list_returns_pagination_metadata(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        for i in range(5):
            create_app(client, headers, {**APP_PAYLOAD, "company": f"Company {i}"})
        resp = client.get("/api/applications?page=1&page_size=3", headers=headers)
        data = resp.json()
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 3
        assert data["total_pages"] == 2
        assert len(data["items"]) == 3

    def test_search_by_company(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        create_app(client, headers, {**APP_PAYLOAD, "company": "Google"})
        create_app(client, headers, {**APP_PAYLOAD, "company": "Meta"})
        resp = client.get("/api/applications?search=google", headers=headers)
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["company"] == "Google"

    def test_filter_by_status(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        create_app(client, headers, {**APP_PAYLOAD, "status": "Applied"})
        create_app(client, headers, {**APP_PAYLOAD, "status": "Interview"})
        resp = client.get("/api/applications?status=Interview", headers=headers)
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "Interview"

    def test_filter_by_job_type(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        create_app(client, headers, {**APP_PAYLOAD, "job_type": "Remote"})
        create_app(client, headers, {**APP_PAYLOAD, "job_type": "Full-Time"})
        resp = client.get("/api/applications?job_type=Remote", headers=headers)
        data = resp.json()
        assert data["total"] == 1


class TestGetSingleApplication:

    def test_get_own_application(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        created = create_app(client, headers).json()
        resp = client.get(f"/api/applications/{created['id']}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_not_found(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.get("/api/applications/99999", headers=headers)
        assert resp.status_code == 404

    def test_user_cannot_access_other_users_application(self, client):
        """Security: user B cannot read user A's applications."""
        register_user(client, email="user_a@example.com")
        register_user(client, name="User B", email="user_b@example.com")

        headers_a = get_auth_headers(client, email="user_a@example.com")
        headers_b = get_auth_headers(client, email="user_b@example.com")

        created = create_app(client, headers_a).json()
        resp = client.get(f"/api/applications/{created['id']}", headers=headers_b)
        assert resp.status_code == 404  # Not found from B's perspective


class TestUpdateApplication:

    def test_update_status(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        created = create_app(client, headers).json()
        resp = client.put(
            f"/api/applications/{created['id']}",
            json={"status": "Interview"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "Interview"

    def test_update_partial(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        created = create_app(client, headers).json()
        resp = client.put(
            f"/api/applications/{created['id']}",
            json={"notes": "Follow up on Monday"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["notes"] == "Follow up on Monday"
        assert resp.json()["company"] == "Acme Corp"  # unchanged

    def test_cannot_update_other_users_application(self, client):
        register_user(client, email="user_a@example.com")
        register_user(client, name="User B", email="user_b@example.com")
        headers_a = get_auth_headers(client, email="user_a@example.com")
        headers_b = get_auth_headers(client, email="user_b@example.com")
        created = create_app(client, headers_a).json()
        resp = client.put(
            f"/api/applications/{created['id']}",
            json={"status": "Rejected"},
            headers=headers_b,
        )
        assert resp.status_code == 404


class TestDeleteApplication:

    def test_delete_success(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        created = create_app(client, headers).json()
        resp = client.delete(f"/api/applications/{created['id']}", headers=headers)
        assert resp.status_code == 204
        # Verify it is really gone
        resp2 = client.get(f"/api/applications/{created['id']}", headers=headers)
        assert resp2.status_code == 404

    def test_cannot_delete_other_users_application(self, client):
        register_user(client, email="user_a@example.com")
        register_user(client, name="User B", email="user_b@example.com")
        headers_a = get_auth_headers(client, email="user_a@example.com")
        headers_b = get_auth_headers(client, email="user_b@example.com")
        created = create_app(client, headers_a).json()
        resp = client.delete(f"/api/applications/{created['id']}", headers=headers_b)
        assert resp.status_code == 404
