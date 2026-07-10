from datetime import datetime

from pydantic import BaseModel

# Discovery DTOs - shaped to the real schema (see campus_connect_schema.md).
# NOTE: no email field, ever. users.email is never surfaced; the only person
# name we expose is the club leader's full_name. See recommender.scrub_emails()
# for the chat-reply side of that same guarantee.


class ClubOut(BaseModel):
    id: int
    name: str
    category: str
    description: str
    # Derived, not a stored column: popularity signal computed from the club's
    # APPROVED membership count. The recommender uses it only as a small prior.
    activity_score: int
    # Derived: users.full_name of the club's LEADER membership (or created_by).
    leader_name: str
    # Not a schema column yet - optional. Matching falls back to category +
    # description when tags are absent. Kept for forward compatibility.
    tags: list[str] = []


class EventOut(BaseModel):
    id: int
    club_id: int
    title: str
    description: str
    venue: str = ""
    starts_at: datetime | None = None
    # Derived: clubs.name for the event's club_id.
    club_name: str
    # Derived: full_name of that club's leader.
    leader_name: str


class DiscoveryContext(BaseModel):
    clubs: list[ClubOut]
    events: list[EventOut]
