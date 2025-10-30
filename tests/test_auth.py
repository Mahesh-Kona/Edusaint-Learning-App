import json
import pytest

from app.extensions import db


def test_register_and_login(client):
    # Register
    rv = client.post("/api/v1/auth/register", json={"email": "u1@example.com", "password": "secret", "role": "teacher"})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["success"] is True
    assert "access_token" in data and "refresh_token" in data

    # Login
    rv2 = client.post("/api/v1/auth/login", json={"email": "u1@example.com", "password": "secret"})
    assert rv2.status_code == 200
    data2 = rv2.get_json()
    assert data2["success"] is True
    assert "access_token" in data2 and "refresh_token" in data2

    # Refresh
    refresh = data2["refresh_token"]
    rv3 = client.post("/api/v1/auth/refresh", headers={"Authorization": f"Bearer {refresh}"})
    assert rv3.status_code == 200
    d3 = rv3.get_json()
    assert d3["success"] is True and "access_token" in d3
