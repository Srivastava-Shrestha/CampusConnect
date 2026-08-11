"""
The read-only tool registry.

Seven tools, each a pure async function plus a JSON schema. Two properties
hold across the whole registry, and both are enforced structurally rather
than by review:

1. Nothing here mutates. Every tool calls a read method on ClubService,
   EventService or AnnouncementService - .list(), .get(), .my_clubs(),
   .feed(). There is no .create()/.update()/.approve()/.join() in reach, so a
   prompt injection hidden in a club description has no lever to pull. That
   is grounding gate 5.

2. No tool takes an identity parameter. There is no college_id or user_id in
   any input_schema, and additionalProperties is false everywhere, so the
   model cannot request another student's or another college's data. Scope
   comes from `payload` - the JWT claims FastAPI already verified via
   Security(get_user_info, ...) - which every service reads to resolve the
   caller's own college and student record. That is grounding gate 2.

This calls the same ClubService/EventService/AnnouncementService every other
router uses, via the same DI pattern (see app/core/di.py). There is no HTTP
hop, no separate auth surface, and no duplicate copy of the club/event data -
earlier drafts of this module called the deployed API over HTTP because the
AI service's own database had no club/event tables yet. It does now, so this
version calls straight into the same process.

The registry shape here - name, description, input_schema, read_only, fn - is
deliberately the same shape MCP's tools/list and tools/call expect. We are not
shipping an MCP server (decision 4.5 in the architecture report explains why),
but structuring it this way keeps that door a short wrapper away.

recommend_clubs is the notable entry: it wraps the v1 deterministic
recommender. The model does not take over ranking, it decides *when* ranking
should happen. The scoring itself stays pure Python with no network access.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from app.agent.grounding import AllowList, redact_for_model
from app.exceptions import AppException
from app.models import ClubType
from app.services import AnnouncementService, ClubService, EventService
from app.services import recommender as R

# Fields the model is allowed to see. Anything a service adds to its response
# later is invisible until someone deliberately adds it here.
CLUB_FIELDS = [
    "id",
    "name",
    "category",
    "type",
    "description",
    "member_count",
    "head_name",
    "status",
]
CLUB_DETAIL_FIELDS = CLUB_FIELDS + ["links", "head"]
EVENT_FIELDS = [
    "id",
    "club_id",
    "club_name",
    "title",
    "venue",
    "starts_at",
    "ends_at",
    "seats_left",
    "status",
]
EVENT_DETAIL_FIELDS = EVENT_FIELDS + [
    "description",
    "capacity",
    "registration_count",
    "is_registered",
]
ANNOUNCEMENT_FIELDS = [
    "id",
    "club_id",
    "club_name",
    "title",
    "body",
    "category",
    "is_pinned",
    "created_at",
]
# Club heads carry contact fields (email, roll_no, branch, year) that are only
# ever populated for campus admins - see ClubHeadInfo. This student-facing
# tool set never receives that populated version, but we still whitelist
# defensively rather than trust "the field happens to be None right now".
CLUB_HEAD_FIELDS = ["student_id", "full_name"]


@dataclass
class Tool:
    """One callable capability offered to the model."""

    name: str
    description: str
    input_schema: dict
    fn: Callable
    read_only: bool = True

    def to_anthropic_schema(self) -> dict:
        """
        The tool definition sent to the Messages API.

        strict=True plus additionalProperties=false means the API guarantees
        the tool input validates against this schema, which is what let us
        stop hand-repairing malformed JSON (decision 4.12).
        """
        return {
            "name": self.name,
            "description": self.description,
            "strict": True,
            "input_schema": self.input_schema,
        }


@dataclass
class Services:
    """The three read services every tool draws on, bundled for one turn."""

    club: ClubService
    event: EventService
    announcement: AnnouncementService


def _dump(items) -> list:
    """Pydantic response models -> plain dicts, JSON-safe (datetimes, enums)."""
    return [item.model_dump(mode="json") for item in items]


def _dump_one(item) -> dict:
    return item.model_dump(mode="json") if item is not None else {}


# ---------------------------------------------------------------------------
# Tool implementations
#
# Every function takes (payload, services, allow_list, **model_supplied_args)
# and returns a JSON-serialisable dict. They never raise: a service error
# comes back as {"error": ...} so the loop can hand the model an is_error
# tool result and keep going with whatever else worked.
# ---------------------------------------------------------------------------


async def _search_clubs(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    club_type = kwargs.get("club_type")
    try:
        rows = await services.club.list(
            payload,
            search=kwargs.get("query"),
            category=kwargs.get("category"),
            type=ClubType(club_type) if club_type else None,
        )
    except AppException as exc:
        return {"error": exc.message}

    dumped = _dump(rows)
    allow_list.add_many("club", dumped, "id", "name")
    return {
        "count": len(dumped),
        "clubs": redact_for_model(dumped, CLUB_FIELDS),
    }


async def _get_club(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    try:
        club = await services.club.get(payload, kwargs["club_id"])
    except AppException as exc:
        return {"error": exc.message}

    row = _dump_one(club)
    allow_list.add("club", row.get("id"), row.get("name"))
    if row.get("head"):
        row["head"] = {k: v for k, v in row["head"].items() if k in CLUB_HEAD_FIELDS}
    projected = redact_for_model([row], CLUB_DETAIL_FIELDS)
    return {"club": projected[0] if projected else {}}


async def _get_my_clubs(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    try:
        rows = await services.club.my_clubs(payload)
    except AppException as exc:
        return {"error": exc.message}

    dumped = _dump(rows)
    allow_list.add_many("club", dumped, "id", "name")
    return {
        "count": len(dumped),
        "memberships": redact_for_model(
            dumped,
            ["id", "name", "category", "membership_role", "membership_status"],
        ),
    }


async def _search_events(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    try:
        rows = await services.event.list(
            payload,
            club_id=kwargs.get("club_id"),
            search=kwargs.get("query"),
            upcoming_only=kwargs.get("upcoming_only", True),
        )
    except AppException as exc:
        return {"error": exc.message}

    dumped = _dump(rows)
    allow_list.add_many("event", dumped, "id", "title")
    return {
        "count": len(dumped),
        "events": redact_for_model(dumped, EVENT_FIELDS),
    }


async def _get_event(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    try:
        event = await services.event.get(payload, kwargs["event_id"])
    except AppException as exc:
        return {"error": exc.message}

    row = _dump_one(event)
    allow_list.add("event", row.get("id"), row.get("title"))
    if row.get("club_id") and row.get("club_name"):
        allow_list.add("club", row["club_id"], row["club_name"])
    projected = redact_for_model([row], EVENT_DETAIL_FIELDS)
    return {"event": projected[0] if projected else {}}


async def _get_announcements(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    try:
        rows = await services.announcement.feed(
            payload,
            club_id=kwargs.get("club_id"),
            limit=min(int(kwargs.get("limit", 10)), 20),
        )
    except AppException as exc:
        return {"error": exc.message}

    dumped = _dump(rows)
    return {
        "count": len(dumped),
        "announcements": redact_for_model(dumped, ANNOUNCEMENT_FIELDS),
    }


async def _recommend_clubs(payload: dict, services: Services, allow_list: AllowList, **kwargs) -> dict:
    """
    The deterministic recommender, exposed as a tool.

    This is the architectural hinge of v2. Ranking authority stays in
    select_recommendations(), which is pure, offline-testable and already
    covered by the v1 suite. What the model gains is the judgement of *when*
    ranking is the right move - not the power to rank.
    """
    interest_text = (kwargs.get("interest_text") or "").strip()
    if not interest_text:
        return {"error": "interest_text is required and must not be empty."}

    try:
        clubs = await services.club.list(payload)
    except AppException as exc:
        return {"error": exc.message}

    try:
        events = await services.event.list(payload, upcoming_only=True)
    except AppException:
        events = []

    # Shape the service rows into what the v1 recommender expects. It scores
    # on name/category/description/tags and an activity_score popularity
    # prior; member_count is the same signal ClubListItem already carries.
    scored_clubs = [
        {
            "id": club.id,
            "name": club.name,
            "category": club.category,
            "description": club.description,
            "tags": [],
            "activity_score": club.member_count,
            "leader_name": club.head_name,
        }
        for club in clubs
    ]

    # EventListItem carries no description (only EventDetailResponse does),
    # so the event scorer sees title-only text here - a real but small
    # accuracy loss versus a second detail fetch per event, which would
    # multiply calls for a rarely-used fallback path.
    scored_events = [
        {
            "id": event.id,
            "club_id": event.club_id,
            "title": event.title,
            "description": "",
            "club_name": event.club_name,
            "leader_name": "",
        }
        for event in events
    ]

    profile = {
        "interests": [interest_text],
        "hobbies": [],
        "reason": interest_text,
        "branch": "",
        "year": 0,
    }

    outcome = R.select_recommendations(profile, scored_clubs, scored_events)

    items = outcome.get("items", [])[:3]
    kind = outcome.get("kind", "clubs")

    # Register whatever the ranker chose, so the model may name it.
    if kind == "event_fallback":
        allow_list.add_many("event", items, "id", "title")
    else:
        allow_list.add_many("club", items, "id", "name")

    # _score is internal ranking detail; strip it before the model sees it.
    cleaned = [{k: v for k, v in item.items() if k != "_score"} for item in items]

    return {
        "kind": kind,
        "count": len(cleaned),
        "items": cleaned,
        "note": outcome.get("message", ""),
    }


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------

REGISTRY: dict = {}


def _register(tool: Tool) -> None:
    REGISTRY[tool.name] = tool


_register(
    Tool(
        name="recommend_clubs",
        description=(
            "Rank this college's clubs against a student's stated interests using the "
            "deterministic Campus Connect recommender. Use this whenever the student "
            "describes what they enjoy or asks what they should join, rather than "
            "picking clubs yourself. Falls back to relevant events, then to the most "
            "active clubs, when nothing matches well."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "interest_text": {
                    "type": "string",
                    "description": "The student's interests in their own words.",
                },
            },
            "required": ["interest_text"],
            "additionalProperties": False,
        },
        fn=_recommend_clubs,
    )
)

_register(
    Tool(
        name="search_clubs",
        description=(
            "Search active clubs in this student's college by keyword, category or "
            "type. Use this to look up a club the student named, or to browse a "
            "category. For open-ended 'what should I join' questions prefer "
            "recommend_clubs."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Free-text search over club name and description.",
                },
                "category": {
                    "type": "string",
                    "description": "Optional category filter, e.g. technology, arts, sports.",
                },
                "club_type": {
                    "type": "string",
                    "enum": ["OFFICIAL", "UNOFFICIAL"],
                    "description": "Optional club type filter.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        fn=_search_clubs,
    )
)

_register(
    Tool(
        name="get_club",
        description=(
            "Fetch full detail for one club by id: description, member count, "
            "category, and who heads it. Call this after search_clubs or "
            "recommend_clubs when the student wants to know more about a specific club."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "club_id": {
                    "type": "integer",
                    "description": "The club's id, taken from an earlier tool result.",
                },
            },
            "required": ["club_id"],
            "additionalProperties": False,
        },
        fn=_get_club,
    )
)

_register(
    Tool(
        name="get_my_clubs",
        description=(
            "List the clubs this student has already joined, with their role and "
            "membership status. Call this before recommending, so you never suggest "
            "something they are already in, and to answer 'am I in X?' questions. "
            "Also the way to get club ids for the student's own clubs."
        ),
        input_schema={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        fn=_get_my_clubs,
    )
)

_register(
    Tool(
        name="search_events",
        description=(
            "Search published events in this student's college. Use upcoming_only to "
            "restrict to events that have not happened yet, and club_id to list one "
            "club's events. Call this for any question about what is happening, when, "
            "or where."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Free-text search over event title.",
                },
                "club_id": {
                    "type": "integer",
                    "description": "Optional: only events hosted by this club.",
                },
                "upcoming_only": {
                    "type": "boolean",
                    "description": "Default true. Set false to include past events.",
                },
            },
            "required": [],
            "additionalProperties": False,
        },
        fn=_search_events,
    )
)

_register(
    Tool(
        name="get_event",
        description=(
            "Fetch full detail for one event by id: description, venue, start and end "
            "time, capacity, seats left, and whether this student is already "
            "registered. Call this when the student asks about a specific event."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "integer",
                    "description": "The event's id, taken from an earlier tool result.",
                },
            },
            "required": ["event_id"],
            "additionalProperties": False,
        },
        fn=_get_event,
    )
)

_register(
    Tool(
        name="get_announcements",
        description=(
            "Read recent club announcements. Pass club_id to scope to one club - "
            "usually an id you got from get_my_clubs. Call this for 'what's new' or "
            "'any updates from my clubs' questions."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "club_id": {
                    "type": "integer",
                    "description": "Optional: only announcements from this club.",
                },
                "limit": {
                    "type": "integer",
                    "description": "How many to return, maximum 20. Default 10.",
                },
            },
            "required": [],
            "additionalProperties": False,
        },
        fn=_get_announcements,
    )
)


def anthropic_tool_schemas() -> list:
    """Every tool definition, in the shape the Messages API expects."""
    return [tool.to_anthropic_schema() for tool in REGISTRY.values()]


async def execute(
    name: str,
    arguments: dict,
    payload: dict,
    services: Services,
    allow_list: AllowList,
) -> Any:
    """
    Run one tool by name.

    Unknown names and unexpected exceptions both come back as an error dict
    rather than propagating, because the loop must always be able to answer a
    tool_use block with a matching tool_result - the API rejects the follow-up
    request otherwise.
    """
    tool = REGISTRY.get(name)
    if tool is None:
        return {"error": "No tool named " + str(name) + "."}

    try:
        return await tool.fn(payload, services, allow_list, **(arguments or {}))
    except TypeError as exc:
        return {"error": "Bad arguments for " + name + ": " + str(exc)}
    except Exception as exc:  # noqa: BLE001 - a tool must never kill the turn
        return {"error": "Tool " + name + " failed: " + str(exc)}
