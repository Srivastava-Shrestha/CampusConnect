"""
Temporary stand-in for the discovery context, shaped to the real schema
(campus_connect_schema.md): APPROVED clubs + upcoming events for a college.

Once the Club / Event / Membership tables are populated, replace
get_discovery_context() with a real query and delete this file. The real
query should return, scoped to college_id:
  - clubs WHERE status = 'APPROVED' AND college_id = :cid
  - events of those clubs WHERE starts_at >= now()  (upcoming only)
and compute the two DERIVED fields the recommender/DTOs expect:
  - activity_score  = count of APPROVED memberships for the club
  - leader_name     = users.full_name of the club's LEADER membership
                      (fallback: created_by student's full_name)
  - club_name       = clubs.name for the event's club_id
There is deliberately no email field and no public/private event flag -
the schema has neither. Every caller depends only on the dict shape below.
"""
from __future__ import annotations

from datetime import datetime, timedelta

_NOW = datetime(2026, 7, 10, 12, 0, 0)


# activity_score / leader_name / club_name below are DERIVED values (see the
# module docstring), inlined here as plausible fixtures - they are not stored
# columns on the clubs/events tables.
_MOCK_CLUBS = [
    {
        "id": 1,
        "college_id": 1,
        "name": "Robotics & Automation Club",
        "category": "technology",
        "description": "Build real robots, compete in national-level challenges, and work on automation projects with peers.",
        "activity_score": 92,
        "leader_name": "Aayansh Yadav",
        "tags": ["robotics", "iot", "automation"],
    },
    {
        "id": 2,
        "college_id": 1,
        "name": "Coding Society",
        "category": "technology",
        "description": "Hackathons, competitive programming contests, and open-source contribution drives every semester.",
        "activity_score": 88,
        "leader_name": "Rishi Agarwal",
        "tags": ["coding", "hackathons", "open-source"],
    },
    {
        "id": 3,
        "college_id": 1,
        "name": "Photography Circle",
        "category": "arts",
        "description": "Weekly photo walks, darkroom sessions, and monthly critique workshops for all skill levels.",
        "activity_score": 60,
        "leader_name": "Neha Pandey",
        "tags": ["photography", "arts"],
    },
    {
        "id": 4,
        "college_id": 1,
        "name": "Music Collective",
        "category": "cultural",
        "description": "Jam sessions, open mic nights, and collaborative song writing across all genres and instruments.",
        "activity_score": 54,
        "leader_name": "Divya Mishra",
        "tags": ["music", "performance"],
    },
    {
        "id": 5,
        "college_id": 1,
        "name": "Debate & Literary Society",
        "category": "literature",
        "description": "Weekly debates, creative writing circles, and public speaking practice for every experience level.",
        "activity_score": 40,
        "leader_name": "Simran Joshi",
        "tags": ["debate", "writing", "poetry"],
    },
    {
        "id": 6,
        "college_id": 1,
        "name": "Astronomy Club",
        "category": "science",
        "description": "Stargazing nights, telescope building, and talks on space missions for curious minds.",
        "activity_score": 30,
        "leader_name": "Pratham Verma",
        "tags": ["astronomy", "space", "science"],
    },
    {
        "id": 7,
        "college_id": 1,
        "name": "Sports Council",
        "category": "sports",
        "description": "Coordinates inter-college tournaments, fitness events, and weekly sports leagues.",
        "activity_score": 70,
        "leader_name": "Varun Tiwari",
        "tags": ["sports", "fitness"],
    },
    {
        "id": 8,
        "college_id": 1,
        "name": "Gaming Guild",
        "category": "gaming",
        "description": "Casual and competitive gaming nights, esports scrims, and tournament watch parties.",
        "activity_score": 45,
        "leader_name": "Aryan Kumar",
        "tags": ["gaming", "esports"],
    },
]

_MOCK_EVENTS = [
    {
        "id": 1,
        "college_id": 1,
        "club_id": 1,
        "title": "Automation Hackathon 2026",
        "description": "Build an automation solution in 8 hours. Teams of 2 to 4 students, all experience levels welcome.",
        "venue": "Seminar Hall, Block A",
        "starts_at": _NOW + timedelta(days=9),
        "club_name": "Robotics & Automation Club",
        "leader_name": "Aayansh Yadav",
    },
    {
        "id": 2,
        "college_id": 1,
        "club_id": 6,
        "title": "Stargazing Night",
        "description": "An evening of telescope viewing and a short talk on the summer sky.",
        "venue": "Rooftop, Science Block",
        "starts_at": _NOW + timedelta(days=4),
        "club_name": "Astronomy Club",
        "leader_name": "Pratham Verma",
    },
    {
        "id": 3,
        "college_id": 1,
        "club_id": 4,
        "title": "Open Mic Night",
        "description": "An open stage for music, poetry, and stand-up across every genre.",
        "venue": "Amphitheatre",
        "starts_at": _NOW + timedelta(days=2),
        "club_name": "Music Collective",
        "leader_name": "Divya Mishra",
    },
]


def get_discovery_context(college_id: int) -> tuple[list[dict], list[dict]]:
    clubs = [c for c in _MOCK_CLUBS if c["college_id"] == college_id]
    events = [e for e in _MOCK_EVENTS if e["college_id"] == college_id]
    return clubs, events
