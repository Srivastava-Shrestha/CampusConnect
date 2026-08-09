import pytest
from datetime import datetime, timedelta, timezone

from app.models import Certificate, Event, RegistrationResult


def future_time(hours: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


@pytest.fixture(autouse=True)
def mock_storage_url(monkeypatch):
    """No S3 access available — stub storage.get_url() so certificate download tests don't need real AWS."""
    from app.core.storage import storage
    monkeypatch.setattr(storage, "get_url", lambda key, signed=False, expires_in=3600: f"https://fake-s3.test/{key}")


# ==== fixtures ====

@pytest.fixture
async def leader(client, seed_college):
    """A student who owns an active club. Yields (headers, club_id)."""
    payload = {
        "email": "cert-leader@knit.edu.in",
        "full_name": "Cert Club Leader",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT",
    }
    signup = await client.post("/auth/signup", json=payload)
    headers = {"Authorization": f"Bearer {signup.json()['access_token']}"}

    payload = {
        "name": "Cert Robotics Club",
        "description": "A club for building robots and breaking budgets",
        "category": "Technical",
        "type": "UNOFFICIAL",
    }
    club = await client.post("/clubs", headers=headers, json=payload)
    return headers, club.json()["id"]


@pytest.fixture
async def member(client, seed_college, leader):
    """An approved member of the leader's club."""
    leader_headers, club_id = leader
    payload = {
        "email": "cert-member@knit.edu.in",
        "full_name": "Cert Club Member",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT",
    }
    signup = await client.post("/auth/signup", json=payload)
    headers = {"Authorization": f"Bearer {signup.json()['access_token']}"}

    join = await client.post(f"/clubs/{club_id}/join", headers=headers)
    payload = {"action": "APPROVED"}
    await client.patch(
        f"/clubs/{club_id}/requests/{join.json()['id']}",
        headers=leader_headers,
        json=payload,
    )
    return headers


@pytest.fixture
async def second_member(client, leader):
    """Another approved member of the leader's club, distinct from `member`."""
    leader_headers, club_id = leader
    payload = {
        "email": "cert-second@knit.edu.in",
        "full_name": "Cert Second Member",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT",
    }
    signup = await client.post("/auth/signup", json=payload)
    headers = {"Authorization": f"Bearer {signup.json()['access_token']}"}

    join = await client.post(f"/clubs/{club_id}/join", headers=headers)
    approve_payload = {"action": "APPROVED"}
    await client.patch(
        f"/clubs/{club_id}/requests/{join.json()['id']}",
        headers=leader_headers, json=approve_payload,
    )
    return headers


@pytest.fixture
async def outsider(client, seed_college):
    """A student of the same college who belongs to no club."""
    payload = {
        "email": "cert-outsider@knit.edu.in",
        "full_name": "Cert Outsider Student",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT",
    }
    signup = await client.post("/auth/signup", json=payload)
    return {"Authorization": f"Bearer {signup.json()['access_token']}"}


@pytest.fixture
async def two_checked_in(client, db_session, leader, member, second_member):
    """Two students registered and checked in, event already started."""
    leader_headers, club_id = leader
    payload = {
        "club_id": club_id,
        "title": "Line Follower Workshop",
        "description": "Hands-on session on building a line follower bot",
        "venue": "Lab 204, Main Block",
        "starts_at": future_time(2),
        "ends_at": future_time(4),
    }
    create = await client.post("/events", headers=leader_headers, json=payload)
    event_id = create.json()["id"]
    await client.patch(f"/events/{event_id}/publish", headers=leader_headers)

    first = await client.post(f"/events/{event_id}/register", headers=member)
    first_registration_id = first.json()["registration_id"]
    second = await client.post(f"/events/{event_id}/register", headers=second_member)
    second_registration_id = second.json()["registration_id"]

    event = await db_session.get(Event, event_id)
    event.starts_at = datetime.now(timezone.utc) - timedelta(hours=1)
    event.ends_at = datetime.now(timezone.utc) + timedelta(hours=1)
    await db_session.flush()

    await client.patch(
        f"/events/{event_id}/registrations/{first_registration_id}/attendance",
        headers=leader_headers, json={"checked_in": True},
    )
    await client.patch(
        f"/events/{event_id}/registrations/{second_registration_id}/attendance",
        headers=leader_headers, json={"checked_in": True},
    )

    return leader_headers, event_id, first_registration_id, second_registration_id


@pytest.fixture
async def certificate_for_member(db_session, two_checked_in):
    """Directly creates a Certificate row for the winner registration from two_checked_in."""
    _, event_id, member_registration_id, _ = two_checked_in

    certificate = Certificate(
        registration_id=member_registration_id,
        serial="CC-LFW-2026-00001",
        result=RegistrationResult.WINNER,
        issued_at=datetime.now(timezone.utc),
    )
    db_session.add(certificate)
    await db_session.flush()

    return event_id, member_registration_id, certificate


# ==== GET /certificates/me ====

@pytest.mark.asyncio
async def test_my_certificates_returns_earned_certificate(client, certificate_for_member, member):
    """Verify that a student with an earned certificate receives it in their list"""
    response = await client.get("/certificates/me", headers=member)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["serial"] == "CC-LFW-2026-00001"
    assert body[0]["result"] == "WINNER"
    assert "download_url" in body[0]


@pytest.mark.asyncio
async def test_my_certificates_empty_for_student_with_none(client, outsider):
    """Confirm that a student with zero certificates receives an empty list"""
    response = await client.get("/certificates/me", headers=outsider)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_my_certificates_without_token_fails(client):
    """Ensure that listing certificates is rejected without an access token"""
    response = await client.get("/certificates/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_my_certificates_by_non_student_fails(client, admin_token):
    """Ensure that a non-student (e.g. CAMPUS_ADMIN) cannot access the student certificate list"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get("/certificates/me", headers=headers)
    assert response.status_code == 401


# ==== GET /certificates/verify/{serial} (public) ====

@pytest.mark.asyncio
async def test_verify_certificate_valid_serial_no_auth_needed(client, certificate_for_member):
    """Verify that a valid serial is confirmed as authentic without any auth headers"""
    response = await client.get("/certificates/verify/CC-LFW-2026-00001")
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["serial"] == "CC-LFW-2026-00001"
    assert body["result"] == "WINNER"


@pytest.mark.asyncio
async def test_verify_certificate_unknown_serial_fails(client):
    """Confirm that verifying a non-existent serial returns not found"""
    response = await client.get("/certificates/verify/CC-FAKE-9999-00000")
    assert response.status_code == 404


# ==== GET /certificates/{serial}/download ====

@pytest.mark.asyncio
async def test_download_certificate_success(client, certificate_for_member, member):
    """Verify that the owning student receives a signed download URL"""
    _, _, certificate = certificate_for_member
    response = await client.get(f"/certificates/{certificate.serial}/download", headers=member)
    assert response.status_code == 200
    body = response.json()
    assert body["serial"] == certificate.serial
    assert body["filename"] == f"{certificate.serial}.pdf"
    assert body["expires_in"] == 3600
    assert "download_url" in body


@pytest.mark.asyncio
async def test_download_certificate_by_non_owner_fails(client, certificate_for_member, outsider):
    """Ensure that a student who does not own the certificate cannot download it"""
    _, _, certificate = certificate_for_member
    response = await client.get(f"/certificates/{certificate.serial}/download", headers=outsider)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_download_certificate_unknown_serial_fails(client, member):
    """Confirm that downloading a non-existent serial returns not found"""
    response = await client.get("/certificates/FAKE-SERIAL/download", headers=member)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_download_certificate_without_token_fails(client, certificate_for_member):
    """Ensure that downloading is rejected without an access token"""
    _, _, certificate = certificate_for_member
    response = await client.get(f"/certificates/{certificate.serial}/download")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"