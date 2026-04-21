import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DISCORD_API_SECRET", "test-secret")
os.environ.setdefault("SCHEDULER_DB_PATH", ":memory:")

from scheduler_api.main import app  # noqa: E402


# Lifespan initialises DB + scheduler; use TestClient as context manager
# so each test gets a fresh lifespan (and a fresh in-memory DB).
def _make_client():
    return TestClient(app)


def test_health():
    with _make_client() as client:
        r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["scheduler"] == "running"


def test_create_reminder_requires_auth():
    with _make_client() as client:
        r = client.post(
            "/reminders",
            json={
                "fire_at": "2099-01-01T12:00:00+00:00",
                "channel_id": "123",
                "guild_id": "456",
                "webhook_url": "https://discord.com/api/webhooks/test",
            },
        )
    assert r.status_code == 403


def test_create_and_get_reminder():
    AUTH = {"Authorization": "Bearer test-secret"}
    with _make_client() as client:
        r = client.post(
            "/reminders",
            json={
                "fire_at": "2099-01-01T12:00:00+00:00",
                "channel_id": "123",
                "guild_id": "456",
                "webhook_url": "https://discord.com/api/webhooks/test",
            },
            headers=AUTH,
        )
        assert r.status_code == 201
        reminder_id = r.json()["reminder_id"]

        r2 = client.get(f"/reminders/{reminder_id}", headers=AUTH)
        assert r2.status_code == 200
        assert r2.json()["status"] == "scheduled"


def test_reminder_missing_destination():
    AUTH = {"Authorization": "Bearer test-secret"}
    with _make_client() as client:
        r = client.post(
            "/reminders",
            json={
                "fire_at": "2099-01-01T12:00:00+00:00",
                "channel_id": "123",
                "guild_id": "456",
            },
            headers=AUTH,
        )
    assert r.status_code == 422


def test_cancel_reminder():
    AUTH = {"Authorization": "Bearer test-secret"}
    with _make_client() as client:
        r = client.post(
            "/reminders",
            json={
                "fire_at": "2099-06-01T12:00:00+00:00",
                "channel_id": "123",
                "guild_id": "456",
                "webhook_url": "https://discord.com/api/webhooks/test",
            },
            headers=AUTH,
        )
        reminder_id = r.json()["reminder_id"]

        r2 = client.delete(f"/reminders/{reminder_id}", headers=AUTH)
        assert r2.status_code == 204
