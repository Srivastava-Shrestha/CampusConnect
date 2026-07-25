import pytest


@pytest.mark.asyncio
async def test_signup_success(client, seed_college):
    """Student signup succeeds when college exists for their email domain"""
    payload = {
        "email": "pawan.kumar@knit.edu.in",
        "full_name": "Pawan Kumar",
        "password": "Pawan@123",
        "confirm_password": "Pawan@123",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body


@pytest.mark.asyncio
async def test_signup_student_without_college_fails(client):
    """Student signup fails when no college matches their email domain"""
    payload = {
        "email": "someone@unknown-domain.edu",
        "full_name": "Someone Unknown",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_signup_duplicate_email_fails(client, seed_college):
    """Signup fails when email is already registered"""
    payload = {
        "email": "rohit.mehta@knit.edu.in",
        "full_name": "Rohit Mehta",
        "password": "Rohit@123",
        "confirm_password": "Rohit@123",
        "role": "STUDENT"
    }
    await client.post("/auth/signup", json=payload)
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_signup_password_mismatch_fails(client, seed_college):
    """Signup fails when password and confirm_password differ"""
    payload = {
        "email": "amit.verma@knit.edu.in",
        "full_name": "Amit Verma",
        "password": "Amit@123",
        "confirm_password": "Different@123",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_invalid_email_fails(client):
    """Signup fails with a malformed email"""
    payload = {
        "email": "not-an-email",
        "full_name": "Vikram Singh",
        "password": "Vikram@123",
        "confirm_password": "Vikram@123",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_short_name_fails(client):
    """Signup fails when full_name is too short"""
    payload = {
        "email": "raj.patel@knit.edu.in",
        "full_name": "Raj",
        "password": "Raj@12345",
        "confirm_password": "Raj@12345",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_short_password_fails(client):
    """Signup fails when password is too short"""
    payload = {
        "email": "suresh.rao@knit.edu.in",
        "full_name": "Suresh Rao",
        "password": "abc123",
        "confirm_password": "abc123",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_missing_fields_fails(client):
    """Signup fails when required fields are missing"""
    payload = {
        "email": "karan.gupta@knit.edu.in",
        "password": "Karan@123"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_signup_empty_payload_fails(client):
    """Signup fails when the request body is completely empty"""
    payload = {}
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_signup_invalid_role_fails(client):
    """Signup fails when role is not STUDENT or CAMPUS_ADMIN"""
    payload = {
        "email": "someone@knit.edu.in",
        "full_name": "Someone Random",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "SUPERUSER"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_signup_admin_success_new_college(client):
    """Admin signup succeeds when no college exists yet for their domain"""
    payload = {
        "email": "admin@newcollege.edu",
        "full_name": "Admin User",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_signup_campus_admin_with_existing_college_fails(client, seed_college):
    """Admin signup fails if a college already exists for that domain"""
    payload = {
        "email": "admin.office@knit.edu.in",
        "full_name": "Admin Office",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 409
    
@pytest.mark.asyncio
async def test_signup_subdomain_of_college_matches(client, seed_college):
    """Signup succeeds when the email is a subdomain of an existing college"""
    payload = {
        "email": "student@cs.knit.edu.in",
        "full_name": "Subdomain Student",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_success(client, seed_college):
    """Login succeeds with correct email and password"""
    payload = {
        "email": "manoj.tiwari@knit.edu.in",
        "full_name": "Manoj Tiwari",
        "password": "Manoj@123",
        "confirm_password": "Manoj@123",
        "role": "STUDENT"
    }
    await client.post("/auth/signup", json=payload)

    payload = {
        "email": "manoj.tiwari@knit.edu.in",
        "password": "Manoj@123"
    }
    response = await client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password_fails(client, seed_college):
    """Login fails with correct email but wrong password"""
    payload = {
        "email": "deepak.yadav@knit.edu.in",
        "full_name": "Deepak Yadav",
        "password": "Deepak@123",
        "confirm_password": "Deepak@123",
        "role": "STUDENT"
    }
    await client.post("/auth/signup", json=payload)

    payload = {
        "email": "deepak.yadav@knit.edu.in",
        "password": "WrongPass1"
    }
    response = await client.post("/auth/login", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user_fails(client):
    """Login fails when email is not registered"""
    payload = {
        "email": "ghost.user@knit.edu.in",
        "password": "Test@1234"
    }
    response = await client.post("/auth/login", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_admin_success(client):
    """Admin login succeeds with correct email and password"""
    payload = {
        "email": "admin.login@newcollege.edu",
        "full_name": "Admin Login User",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    await client.post("/auth/signup", json=payload)

    payload = {
        "email": "admin.login@newcollege.edu",
        "password": "Admin@123"
    }
    response = await client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

