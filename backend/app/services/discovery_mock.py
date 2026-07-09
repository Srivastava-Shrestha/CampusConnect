"""
Temporary stand-in for the discovery context (approved clubs + published
public events, scoped per college) described in the design doc.

There is no Club or Event table in the schema yet (see app/models - only
College, User, Student, CampusAdmin exist). Once those land, replace
get_discovery_context() with a real query - approved clubs + published
events for the given college_id, cached server-side per college with
invalidation on club-approval / event-publish - and delete this file. Every
caller in routers/ai.py and routers/discovery.py only depends on the
(clubs, events) dict shape below, so that swap does not touch anything else.

No email fields anywhere in this data, on purpose - see schemas/discovery.py.
"""
from __future__ import annotations

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
        "title": "Automation Hackathon 2026",
        "description": "Build an automation solution in 8 hours. Teams of 2 to 4 students, all experience levels welcome.",
        "club_name": "Robotics & Automation Club",
        "leader_name": "Aayansh Yadav",
        "visibility": "public",
    },
    {
        "id": 2,
        "college_id": 1,
        "title": "Stargazing Night",
        "description": "An evening of telescope viewing and a short talk on the summer sky.",
        "club_name": "Astronomy Club",
        "leader_name": "Pratham Verma",
        "visibility": "public",
    },
    {
        "id": 3,
        "college_id": 1,
        "title": "Internal Robotics Build Session",
        "description": "Members-only working session on the line-follower robot build.",
        "club_name": "Robotics & Automation Club",
        "leader_name": "Aayansh Yadav",
        "visibility": "members",
    },
    {
        "id": 4,
        "college_id": 1,
        "title": "Open Mic Night",
        "description": "An open stage for music, poetry, and stand-up across every genre.",
        "club_name": "Music Collective",
        "leader_name": "Divya Mishra",
        "visibility": "public",
    },
]


def get_discovery_context(college_id: int) -> tuple[list[dict], list[dict]]:
    clubs = [c for c in _MOCK_CLUBS if c["college_id"] == college_id]
    events = [e for e in _MOCK_EVENTS if e["college_id"] == college_id]
    return clubs, events
