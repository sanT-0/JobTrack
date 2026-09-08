"""
tests/test_auth.py — Tests for registration, login, and authentication.
"""
import pytest
from app.tests.conftest import register_user, get_auth_headers


class TestRegister:

    def test_register_success(self, client):
        resp = register_user(client)
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_email(self, client):
        register_user(client)
        resp = register_user(client)
        assert resp.status_code == 409
        assert "already exists" in resp.json()["detail"]

    def test_register_invalid_email(self, client):
        resp = client.post("/api/auth/register", json={
            "name": "Test", "email": "not-an-email", "password": "password123"
        })
        assert resp.status_code == 422

    def test_register_short_password(self, client):
        resp = client.post("/api/auth/register", json={
            "name": "Test", "email": "x@x.com", "password": "short"
        })
        assert resp.status_code == 422

    def test_register_empty_name(self, client):
        resp = client.post("/api/auth/register", json={
            "name": "   ", "email": "x@x.com", "password": "password123"
        })
        assert resp.status_code == 422


class TestLogin:

    def test_login_success(self, client):
        register_user(client)
        resp = client.post("/api/auth/login", json={
            "email": "test@example.com", "password": "password123"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_login_wrong_password(self, client):
        register_user(client)
        resp = client.post("/api/auth/login", json={
            "email": "test@example.com", "password": "wrongpassword"
        })
        assert resp.status_code == 401

    def test_login_unknown_email(self, client):
        resp = client.post("/api/auth/login", json={
            "email": "nobody@example.com", "password": "password123"
        })
        assert resp.status_code == 401

    def test_login_returns_same_error_for_both_failures(self, client):
        """Prevents user enumeration — same error for unknown email and wrong password."""
        register_user(client)
        r1 = client.post("/api/auth/login", json={"email": "nobody@x.com", "password": "password123"})
        r2 = client.post("/api/auth/login", json={"email": "test@example.com", "password": "wrong"})
        assert r1.json()["detail"] == r2.json()["detail"]


class TestMe:

    def test_get_me_authenticated(self, client):
        register_user(client)
        headers = get_auth_headers(client)
        resp = client.get("/api/auth/me", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert "password_hash" not in data  # MUST never be exposed

    def test_get_me_unauthenticated(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code in (401, 403)  # No credentials provided

    def test_get_me_invalid_token(self, client):
        resp = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert resp.status_code == 401
