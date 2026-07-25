import pytest


@pytest.mark.asyncio
async def test_onboarding_success(client, admin_token):
    """Admin can create a college when they have a valid token"""
    payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "Kamla Nehru Institute of Technology"
    }
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["slug"] == "knit"
    assert body["email_suffix"] == "knit.edu.in"


@pytest.mark.asyncio
async def test_onboarding_without_token_fails(client):
    """Cannot create a college without logging in"""
    payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "Kamla Nehru Institute of Technology"
    }
    response = await client.post("/college/onboarding", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_onboarding_with_student_token_fails(client):
    """A student cannot create a college, only an admin can"""
    admin_payload = {
        "email": "seed.admin@somecollege.edu",
        "full_name": "Seed Admin",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    admin_signup = await client.post("/auth/signup", json=admin_payload)
    seed_admin_token = admin_signup.json()["access_token"]

    college_payload = {
        "name": "Some College Institute",
        "email_suffix": "somecollege.edu",
        "description": "Just to create a student for this test"
    }
    await client.post(
        "/college/onboarding",
        json=college_payload,
        headers={"Authorization": f"Bearer {seed_admin_token}"}
    )

    student_payload = {
        "email": "pupil@somecollege.edu",
        "full_name": "Pupil Student",
        "password": "Pupil@123",
        "confirm_password": "Pupil@123",
        "role": "STUDENT"
    }
    student_signup = await client.post("/auth/signup", json=student_payload)
    student_token = student_signup.json()["access_token"]

    onboarding_payload = {
        "name": "Another College Institute",
        "email_suffix": "another.edu",
        "description": "A student should not be able to do this"
    }
    response = await client.post(
        "/college/onboarding",
        json=onboarding_payload,
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_onboarding_duplicate_college_fails(client, admin_token):
    """Cannot create a college that already exists"""
    college_payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "Kamla Nehru Institute of Technology"
    }
    await client.post(
        "/college/onboarding",
        json=college_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    admin_payload = {
        "email": "second.admin@differentdomain.edu",
        "full_name": "Second Admin",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    second_admin = await client.post("/auth/signup", json=admin_payload)
    second_token = second_admin.json()["access_token"]

    response = await client.post(
        "/college/onboarding",
        json=college_payload,
        headers={"Authorization": f"Bearer {second_token}"}
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_onboarding_missing_fields_fails(client, admin_token):
    """Cannot create a college if required fields are missing"""
    payload = {"name": "Kamla Nehru Institute of Technology"}
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_onboarding_invalid_token_fails(client):
    """Cannot create a college with a fake token"""
    payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "Kamla Nehru Institute of Technology"
    }
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_onboarding_short_name_fails(client, admin_token):
    """College name must be long enough"""
    payload = {
        "name": "KN",
        "email_suffix": "shortname.edu.in",
        "description": "Name is too short here"
    }
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_onboarding_short_description_fails(client, admin_token):
    """College description must be long enough"""
    payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "shortdesc.edu.in",
        "description": "Hi"
    }
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_onboarding_slug_collision_increments(client, admin_token):
    """College onboarding gets a numbered slug when the prefix is already taken"""
    first_payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "First college with this slug prefix"
    }
    await client.post(
        "/college/onboarding",
        json=first_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    admin_payload = {
        "email": "second.admin@knit.org.in",
        "full_name": "Second Admin",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    second_admin = await client.post("/auth/signup", json=admin_payload)
    second_token = second_admin.json()["access_token"]

    second_payload = {
        "name": "Kamla Nehru Institute Org",
        "email_suffix": "knit.org.in",
        "description": "Second college with colliding slug prefix"
    }
    response = await client.post(
        "/college/onboarding",
        json=second_payload,
        headers={"Authorization": f"Bearer {second_token}"}
    )
    assert response.status_code == 200
    assert response.json()["slug"] == "knit-2"

@pytest.mark.asyncio
async def test_onboarding_third_slug_collision_increments_further(client, admin_token):
    """Third college with the same prefix gets slug knit-3"""
    first_payload = {
        "name": "Kamla Nehru Institute of Technology",
        "email_suffix": "knit.edu.in",
        "description": "First college with this slug prefix"
    }
    await client.post(
        "/college/onboarding",
        json=first_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    admin_payload_two = {
        "email": "second.admin@knit.org.in",
        "full_name": "Second Admin",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    second_admin = await client.post("/auth/signup", json=admin_payload_two)
    second_token = second_admin.json()["access_token"]

    second_payload = {
        "name": "Kamla Nehru Institute Org",
        "email_suffix": "knit.org.in",
        "description": "Second college with colliding slug prefix"
    }
    await client.post(
        "/college/onboarding",
        json=second_payload,
        headers={"Authorization": f"Bearer {second_token}"}
    )

    admin_payload_three = {
        "email": "third.admin@knit.ac.in",
        "full_name": "Third Admin",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    third_admin = await client.post("/auth/signup", json=admin_payload_three)
    third_token = third_admin.json()["access_token"]

    third_payload = {
        "name": "Kamla Nehru Institute AC",
        "email_suffix": "knit.ac.in",
        "description": "Third college with colliding slug prefix"
    }
    response = await client.post(
        "/college/onboarding",
        json=third_payload,
        headers={"Authorization": f"Bearer {third_token}"}
    )
    assert response.status_code == 200
    assert response.json()["slug"] == "knit-3"

@pytest.mark.asyncio
async def test_onboarding_malformed_email_suffix_fails(client, admin_token):
    """Onboarding fails with an invalid domain-like suffix"""
    payload = {
        "name": "Some Random College",
        "email_suffix": "not_a_domain",
        "description": "Testing malformed suffix"
    }
    response = await client.post(
        "/college/onboarding",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in (400, 422)