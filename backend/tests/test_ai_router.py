from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_club_finder_returns_clubs_for_a_matching_interest():
    response = client.post("/api/v1/ai/club-finder", json={"interest_text": "robotics and drones"})

    assert response.status_code == 200
    data = response.json()
    assert data["kind"] == "clubs"
    assert data["items"][0]["reason"]


def test_club_finder_skips_the_llm_call_when_interest_text_is_empty():
    with patch("app.routers.ai.call_finder") as mock_call_finder:
        response = client.post("/api/v1/ai/club-finder", json={"interest_text": ""})

        assert response.status_code == 200
        mock_call_finder.assert_not_called()


def test_club_finder_falls_back_to_a_deterministic_reason_when_the_llm_fails():
    with patch("app.routers.ai.call_finder", side_effect=Exception("boom")):
        response = client.post("/api/v1/ai/club-finder", json={"interest_text": "robotics"})

        assert response.status_code == 200
        assert response.json()["items"][0]["reason"] == "Matches your interests."


def test_club_finder_falls_back_to_popularity_for_an_unmatched_interest():
    response = client.post("/api/v1/ai/club-finder", json={"interest_text": "underwater basket weaving"})

    assert response.status_code == 200
    assert response.json()["kind"] == "popularity"


def test_club_finder_event_fallback_surfaces_event_with_derived_fields():
    # No club matches "trivia", but an event does - proves the full endpoint
    # path for events, including the derived club_name / leader_name fields.
    clubs = [{"id": 1, "name": "Chess Club", "category": "sports",
              "description": "board games", "activity_score": 5, "leader_name": "Lead", "tags": []}]
    events = [{"id": 9, "club_id": 1, "title": "Campus Trivia Night",
               "description": "a fun trivia quiz evening", "venue": "Hall",
               "starts_at": None, "club_name": "Quiz Club", "leader_name": "Meera"}]

    with patch("app.routers.ai.get_discovery_context", return_value=(clubs, events)):
        response = client.post("/api/v1/ai/club-finder", json={"interest_text": "trivia quiz"})

    assert response.status_code == 200
    data = response.json()
    assert data["kind"] == "event_fallback"
    assert data["items"][0]["club_name"] == "Quiz Club"
    assert data["items"][0]["leader_name"] == "Meera"
    assert "@" not in response.text


def test_club_finder_payload_never_includes_an_email():
    response = client.post("/api/v1/ai/club-finder", json={"interest_text": "robotics"})

    assert "@" not in response.text


def test_chat_reply_never_leaks_a_raw_entity_tag_for_an_unknown_id():
    response = client.post("/api/v1/ai/chat", json={"messages": [{"role": "user", "content": "hi"}]})

    assert response.status_code == 200
    assert "[[" not in response.json()["reply"]


def test_chat_reply_never_includes_an_email():
    response = client.post("/api/v1/ai/chat", json={"messages": [{"role": "user", "content": "hi"}]})

    assert "@" not in response.json()["reply"]
