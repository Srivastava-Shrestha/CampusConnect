from pydantic import BaseModel

# Discovery DTOs - NOTE: no email field, ever. See app/services/recommender.py
# scrub_emails() for the chat-reply side of that same guarantee.


class ClubOut(BaseModel):
    id: int
    name: str
    category: str
    description: str
    activity_score: int
    leader_name: str
    tags: list[str] = []


class EventOut(BaseModel):
    id: int
    title: str
    description: str
    club_name: str
    leader_name: str
    visibility: str


class DiscoveryContext(BaseModel):
    clubs: list[ClubOut]
    events: list[EventOut]
