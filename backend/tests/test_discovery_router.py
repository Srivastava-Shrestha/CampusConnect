from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_discovery_context_returns_clubs_and_events():
    response = client.get("/api/v1/discovery/context")

    assert response.status_code == 200
    data = response.json()
    assert len(data["clubs"]) > 0
    assert len(data["events"]) > 0


def test_discovery_context_only_has_the_documented_club_fields():
    response = client.get("/api/v1/discovery/context")
    club = response.json()["clubs"][0]

    assert set(club.keys()) == {"id", "name", "category", "description", "activity_score", "leader_name", "tags"}


def test_discovery_context_never_includes_an_email_field():
    response = client.get("/api/v1/discovery/context")

    assert "@" not in response.text
