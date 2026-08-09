import json
from pathlib import Path
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.database import Base, get_db
from app.core.config import settings
from app.models.college import College
from main import app


TEST_DATABASE_URL = settings.TEST_DATABASE_URL
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture()
async def db_session(setup_db) -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def seed_college(db_session: AsyncSession) -> College:
    # student signup needs a college to already exist for their email domain
    college = College(
        name="Test University",
        email_suffix="knit.edu.in",
        slug="test-university"
    )
    db_session.add(college)
    await db_session.flush()
    await db_session.refresh(college)
    return college



_results_log = []
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        outcome = "passed" if call.excinfo is None else "failed"
        _results_log.append({
            "test": item.nodeid,
            "outcome": outcome,
            "error": str(call.excinfo.value) if call.excinfo else None,
        })

def pytest_sessionfinish(session, exitstatus):
    Path("tests/reports").mkdir(parents=True, exist_ok=True)
    Path("tests/reports/results_log.json").write_text(json.dumps(_results_log, indent=2))

@pytest_asyncio.fixture()
async def admin_token(client):
    payload = {
        "email": "admin@newcollege.edu",
        "full_name": "Admin User",
        "password": "Admin@123",
        "confirm_password": "Admin@123",
        "role": "CAMPUS_ADMIN"
    }
    response = await client.post("/auth/signup", json=payload)
    body = response.json()
    return body["access_token"]


@pytest_asyncio.fixture()
async def student_token(client, seed_college):
    payload = {
        "email": "club.student@knit.edu.in",
        "full_name": "Club Student",
        "password": "Student@123",
        "confirm_password": "Student@123",
        "role": "STUDENT"
    }
    response = await client.post("/auth/signup", json=payload)
    body = response.json()
    return body["access_token"]