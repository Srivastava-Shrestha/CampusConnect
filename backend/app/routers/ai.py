from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.schemas.ai import ChatRequest, ChatResponse, ClubFinderRequest
from app.services import recommender as R
from app.services.discovery_mock import get_discovery_context
from app.services.llm_client import call_chat, call_finder, call_message

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


def _user_profile_dict(user: dict) -> dict:
    return {
        "interests": user.get("interests", []),
        "hobbies": user.get("hobbies", []),
        "reason": user.get("reason", ""),
        "branch": user.get("branch", ""),
        "year": user.get("year"),
    }


@router.post("/club-finder")
def club_finder(body: ClubFinderRequest, user: dict = Depends(get_current_user)):
    clubs, events = get_discovery_context(user["college_id"])
    profile = _user_profile_dict(user)

    # What the student just typed drives the ranking, not just the LLM's
    # reason text - otherwise every request scores against the same stored
    # profile and always surfaces the same clubs regardless of input.
    interest_text = body.interest_text.strip()
    if interest_text:
        profile = {**profile, "interests": profile["interests"] + [interest_text]}

    result = R.select_recommendations(profile, clubs, events)

    if not interest_text:
        return result   # nothing typed yet - deterministic order, no LLM call

    if result["kind"] == "clubs":
        top = result["items"][:R.DEFAULT_CFG.top_k]
        allowed = {c["id"] for c in top}
        prompt = R.build_finder_prompt(profile, top)
        try:
            raw = call_finder(prompt, candidate_hash=",".join(map(str, sorted(allowed))))
            reasons = {r["club_id"]: r["reason"] for r in R.validate_finder_json(raw, allowed)}
        except Exception:
            reasons = {}                                  # fallback: deterministic order
        for c in top:
            c["reason"] = reasons.get(c["id"], "Matches your interests.")
        result = {"kind": "clubs", "items": top}

    # The top-level reply is always LLM-phrased when the student typed
    # something - the deterministic string from select_recommendations is
    # only a silent safety net if this call fails.
    message_prompt = R.build_conversational_message_prompt(interest_text, result["kind"], result["items"])
    try:
        result["message"] = call_message(message_prompt)
    except Exception:
        result.setdefault("message", "Here are a few clubs that fit what you described.")

    return result


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, user: dict = Depends(get_current_user)):
    clubs, events = get_discovery_context(user["college_id"])
    available = R.build_chat_available(clubs, events)
    system = R.CHAT_SYSTEM_PROMPT.format(available=available)
    history = [m.model_dump() for m in body.messages][-10:]   # cap context

    raw = call_chat(system, history)

    allowed_map = {("club", c["id"]): c["name"] for c in clubs}
    allowed_map.update({("event", e["id"]): e["title"]
                        for e in events if e.get("visibility") == "public"})
    clean, _unknown = R.resolve_entities(raw, allowed_map)
    return {"reply": R.scrub_emails(clean)}
