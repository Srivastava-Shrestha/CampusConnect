"""
Bring up a throwaway local database with enough data to exercise the AI module.

Why this exists
---------------
Running the app normally needs Postgres plus the alembic migration chain. That
is the right setup for real backend work, but it is a lot of moving parts for
someone who only wants to click through the AI Club Finder and see whether it
answers sensibly. This script creates a single SQLite file instead, builds the
schema straight from the models, and fills it with one college, a handful of
students, six clubs, some events and announcements.

It is a development convenience only. It is never imported by the application,
and nothing in app/ knows it exists.

    cd backend
    uv run python scripts/dev_seed.py

Then log in with any of the accounts printed at the end.

Two things worth knowing:

- The schema comes from Base.metadata.create_all, not from alembic. The
  migrations are written for Postgres and will not run on SQLite. That means
  this database is only as correct as the models, which is fine for clicking
  around but is not a substitute for testing against Postgres.
- The file is deleted and rebuilt on every run, so it is always a clean slate.
"""
from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BACKEND_DIR / "dev.db"

# The engine in app/core/database.py is built at import time from settings, so
# every environment variable has to be in place before anything under app/ is
# imported. Setting them here means the script works even with an empty .env.
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
os.environ.setdefault("TEST_DATABASE_URL", os.environ["DATABASE_URL"])
os.environ.setdefault("JWT_SECRET_KEY", "local-dev-secret-not-for-production")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

# Certificate storage is required by Settings, but nothing this script touches
# uploads anything. Placeholders keep the import working offline.
os.environ.setdefault("AWS_REGION", "ap-south-1")
os.environ.setdefault("S3_BUCKET_NAME", "local-dev-not-used")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "local-dev-not-used")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "local-dev-not-used")

# Same for outbound mail - nothing here sends any.
os.environ.setdefault("SMTP_HOST", "localhost")
os.environ.setdefault("SMTP_PORT", "1025")
os.environ.setdefault("SMTP_USER", "local-dev-not-used")
os.environ.setdefault("SMTP_PASSWORD", "local-dev-not-used")
os.environ.setdefault("MAIL_FROM", "noreply@localhost")

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.models import (  # noqa: E402
    Announcement,
    AnnouncementCategory,
    CampusAdmin,
    Club,
    ClubStatus,
    ClubType,
    College,
    Event,
    EventStatus,
    Membership,
    MembershipRole,
    MembershipStatus,
    Student,
    User,
    UserRole,
)
from app.utils.hashing import hash_password  # noqa: E402

COLLEGE_NAME = "NexMind Institute of Technology"
EMAIL_SUFFIX = "nexmind.edu"
COLLEGE_SLUG = "nexmind-institute-of-technology"
PASSWORD = "password123"


def slugify(name: str) -> str:
    """Match the slug shape the real college onboarding service produces."""
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in name)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


# Six clubs across different categories, so the recommender has something to
# actually discriminate between. Descriptions are deliberately wordy - the
# keyword scoring in services/recommender.py reads them.
CLUB_SEED = [
    {
        "name": "Robotics & Automation",
        "category": "Technology",
        "type": ClubType.OFFICIAL,
        "description": (
            "We build autonomous robots, line followers and drone prototypes. "
            "Members work with Arduino, Raspberry Pi, ROS and embedded C. "
            "We compete in national robotics championships every semester and "
            "run a beginner electronics bootcamp for first years."
        ),
    },
    {
        "name": "Coding Society",
        "category": "Technology",
        "type": ClubType.OFFICIAL,
        "description": (
            "A competitive programming and software engineering community. "
            "Weekly algorithm contests, open source contribution drives, and "
            "hackathons. We cover data structures, machine learning, web "
            "development and interview preparation."
        ),
    },
    {
        "name": "Music Collective",
        "category": "Culture",
        "type": ClubType.OFFICIAL,
        "description": (
            "Instrumentalists, vocalists and producers jamming across genres "
            "from Hindustani classical to indie rock. We run open mic nights, "
            "a recording setup for members, and the annual campus band battle."
        ),
    },
    {
        "name": "Photography Circle",
        "category": "Arts",
        "type": ClubType.UNOFFICIAL,
        "description": (
            "Street, portrait, wildlife and astrophotography. Monthly photo "
            "walks, darkroom and Lightroom editing workshops, and a printed "
            "annual exhibition of member work."
        ),
    },
    {
        "name": "Entrepreneurship Cell",
        "category": "Business",
        "type": ClubType.OFFICIAL,
        "description": (
            "Turning student ideas into startups. Pitch practice, business "
            "model canvas workshops, mentor office hours with founders, and a "
            "demo day with visiting angel investors."
        ),
    },
    {
        "name": "Debate & Literary Society",
        "category": "Culture",
        "type": ClubType.UNOFFICIAL,
        "description": (
            "Parliamentary debate, MUN delegations, creative writing circles "
            "and poetry slams. We train members in public speaking, research "
            "and argumentation for inter-college tournaments."
        ),
    },
]

EVENT_SEED = [
    {
        "club": "Robotics & Automation",
        "title": "Line Follower Build Night",
        "venue": "Tinkering Lab, Block C",
        "days_from_now": 5,
        "capacity": 40,
        "description": (
            "Hands-on session building a line following robot from scratch. "
            "Components provided, no prior experience needed."
        ),
    },
    {
        "club": "Robotics & Automation",
        "title": "Inter-College Robowars Qualifier",
        "venue": "Main Auditorium",
        "days_from_now": 21,
        "capacity": 200,
        "description": "Combat robot qualifiers. Teams of four, 8kg weight class.",
    },
    {
        "club": "Coding Society",
        "title": "48-Hour Campus Hackathon",
        "venue": "Central Library Atrium",
        "days_from_now": 12,
        "capacity": 150,
        "description": (
            "Build anything in 48 hours. Tracks for AI, sustainability and "
            "campus utilities. Mentors from industry on site."
        ),
    },
    {
        "club": "Music Collective",
        "title": "Open Mic Night",
        "venue": "Amphitheatre",
        "days_from_now": 3,
        "capacity": 120,
        "description": "Ten minute slots for anyone who wants the stage.",
    },
    {
        "club": "Photography Circle",
        "title": "Old City Photo Walk",
        "venue": "Meet at Main Gate",
        "days_from_now": 9,
        "capacity": 25,
        "description": "Sunrise street photography walk. Bring any camera.",
    },
    {
        "club": "Entrepreneurship Cell",
        "title": "Founder Fireside: Scaling to 1M Users",
        "venue": "Seminar Hall 2",
        "days_from_now": 15,
        "capacity": 80,
        "description": "A conversation with an alumnus who scaled a consumer app.",
    },
    {
        "club": "Coding Society",
        "title": "Intro to Machine Learning Workshop",
        "venue": "Computer Lab 3",
        "days_from_now": -6,
        "capacity": 60,
        "description": "A past event, kept so the archive is not empty.",
    },
]

ANNOUNCEMENT_SEED = [
    {
        "club": "Robotics & Automation",
        "title": "Lab access extended to 10pm",
        "category": AnnouncementCategory.GENERAL,
        "pinned": True,
        "body": (
            "The tinkering lab is now open until 10pm on weekdays for members "
            "with an active project. Sign the register at the door."
        ),
    },
    {
        "club": "Coding Society",
        "title": "Hackathon registrations close Friday",
        "category": AnnouncementCategory.EVENT_UPDATE,
        "pinned": True,
        "body": "Team registrations for the 48-hour hackathon close this Friday at 6pm.",
    },
    {
        "club": "Music Collective",
        "title": "New recording interface available",
        "category": AnnouncementCategory.RESOURCE,
        "pinned": False,
        "body": "An 8-channel audio interface is now in the practice room for member use.",
    },
]

# The demo student is put in one club only. That is deliberate: it lets you ask
# the assistant "what am I already part of?" and get a checkable answer, and it
# leaves room for it to recommend something new.
DEMO_STUDENT_CLUB = "Photography Circle"

STUDENT_SEED = [
    {"full_name": "Demo Student", "email": f"student@{EMAIL_SUFFIX}", "leads": None},
    {"full_name": "Riya Sharma", "email": f"riya@{EMAIL_SUFFIX}", "leads": "Robotics & Automation"},
    {"full_name": "Arjun Menon", "email": f"arjun@{EMAIL_SUFFIX}", "leads": "Coding Society"},
    {"full_name": "Neha Iyer", "email": f"neha@{EMAIL_SUFFIX}", "leads": "Music Collective"},
    {"full_name": "Kabir Singh", "email": f"kabir@{EMAIL_SUFFIX}", "leads": "Photography Circle"},
    {"full_name": "Ananya Rao", "email": f"ananya@{EMAIL_SUFFIX}", "leads": "Entrepreneurship Cell"},
    {"full_name": "Vikram Nair", "email": f"vikram@{EMAIL_SUFFIX}", "leads": "Debate & Literary Society"},
]


async def reset_schema() -> None:
    """Drop the old file and rebuild every table from the models."""
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except PermissionError:
            # Windows keeps the file locked while uvicorn holds it open, and
            # the raw traceback gives no hint about what to do next.
            print()
            print("  Cannot rebuild the database - the file is in use.")
            print("  Stop the running API (Ctrl+C in its terminal) and try again.")
            print(f"  file: {DB_PATH}")
            print()
            raise SystemExit(1)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def create_user(session, full_name: str, email: str, role: UserRole, college_id):
    """Create a user row plus whichever profile row the role requires."""
    user = User(
        college_id=college_id,
        email=email,
        hashed_password=hash_password(PASSWORD),
        full_name=full_name,
        role=role,
    )
    session.add(user)
    await session.flush()

    if role == UserRole.STUDENT:
        profile = Student(user_id=user.id, interests=[])
    else:
        profile = CampusAdmin(user_id=user.id)

    session.add(profile)
    await session.flush()

    return user, profile


async def seed() -> dict:
    """Fill the empty database and hand back the accounts worth printing."""
    async with SessionLocal() as session:
        college = College(
            name=COLLEGE_NAME,
            email_suffix=EMAIL_SUFFIX,
            slug=slugify(COLLEGE_NAME),
            description="A demo college used for local development of Campus Connect.",
        )
        session.add(college)
        await session.flush()

        await create_user(
            session,
            full_name="Campus Admin",
            email=f"admin@{EMAIL_SUFFIX}",
            role=UserRole.CAMPUS_ADMIN,
            college_id=college.id,
        )

        students_by_name = {}
        for entry in STUDENT_SEED:
            _, student = await create_user(
                session,
                full_name=entry["full_name"],
                email=entry["email"],
                role=UserRole.STUDENT,
                college_id=college.id,
            )
            students_by_name[entry["full_name"]] = student

        # Every club needs a head, so map each club to the student who leads it.
        leader_of = {
            entry["leads"]: students_by_name[entry["full_name"]]
            for entry in STUDENT_SEED
            if entry["leads"]
        }

        clubs_by_name = {}
        for entry in CLUB_SEED:
            head = leader_of[entry["name"]]
            club = Club(
                college_id=college.id,
                club_head=head.id,
                name=entry["name"],
                description=entry["description"],
                category=entry["category"],
                type=entry["type"],
                status=ClubStatus.ACTIVE,
            )
            session.add(club)
            await session.flush()
            clubs_by_name[entry["name"]] = club

            session.add(
                Membership(
                    student_id=head.id,
                    club_id=club.id,
                    role=MembershipRole.LEADER,
                    status=MembershipStatus.APPROVED,
                )
            )

        # Spread the club leaders around as ordinary members of each other's
        # clubs, so member counts differ - the recommender reads that as an
        # activity signal.
        #
        # The demo student is deliberately left out of this and joined to
        # exactly one club below. Being a member of everything would make
        # "recommend me something new" impossible to answer, and "what am I
        # part of?" impossible to eyeball for correctness.
        demo_student = students_by_name["Demo Student"]
        leaders = [s for s in students_by_name.values() if s.id != demo_student.id]

        for index, entry in enumerate(CLUB_SEED):
            club = clubs_by_name[entry["name"]]
            head_id = leader_of[entry["name"]].id
            joiners = [s for s in leaders if s.id != head_id][: 5 - index]

            for student in joiners:
                session.add(
                    Membership(
                        student_id=student.id,
                        club_id=club.id,
                        role=MembershipRole.MEMBER,
                        status=MembershipStatus.APPROVED,
                    )
                )

        session.add(
            Membership(
                student_id=demo_student.id,
                club_id=clubs_by_name[DEMO_STUDENT_CLUB].id,
                role=MembershipRole.MEMBER,
                status=MembershipStatus.APPROVED,
            )
        )

        now = datetime.now(timezone.utc)
        for entry in EVENT_SEED:
            club = clubs_by_name[entry["club"]]
            starts_at = now + timedelta(days=entry["days_from_now"])
            session.add(
                Event(
                    club_id=club.id,
                    created_by=club.club_head,
                    title=entry["title"],
                    description=entry["description"],
                    venue=entry["venue"],
                    starts_at=starts_at,
                    ends_at=starts_at + timedelta(hours=3),
                    capacity=entry["capacity"],
                    status=EventStatus.PUBLISHED,
                )
            )

        for entry in ANNOUNCEMENT_SEED:
            club = clubs_by_name[entry["club"]]
            session.add(
                Announcement(
                    club_id=club.id,
                    author_id=club.club_head,
                    title=entry["title"],
                    body=entry["body"],
                    category=entry["category"],
                    is_pinned=entry["pinned"],
                )
            )

        await session.commit()

        return {
            "slug": college.slug,
            "clubs": len(CLUB_SEED),
            "events": len(EVENT_SEED),
            "students": len(STUDENT_SEED),
        }


async def main() -> None:
    await reset_schema()
    summary = await seed()
    await engine.dispose()

    print()
    print("  Local development database ready")
    print(f"  file      {DB_PATH}")
    print(f"  seeded    {summary['clubs']} clubs, {summary['events']} events, "
          f"{summary['students']} students")
    print()
    print("  Sign in with any of these (all share the same password):")
    print(f"    student   student@{EMAIL_SUFFIX}   {PASSWORD}")
    print(f"    leader    riya@{EMAIL_SUFFIX}      {PASSWORD}   (heads Robotics & Automation)")
    print(f"    admin     admin@{EMAIL_SUFFIX}     {PASSWORD}")
    print()
    print(f"  The AI Club Finder lives at /{summary['slug']}/find-clubs")
    print()
    print("  Start the API against this database with:")
    print('    uv run --env-file .env.local uvicorn main:app --reload --port 8000')
    print()


if __name__ == "__main__":
    asyncio.run(main())
