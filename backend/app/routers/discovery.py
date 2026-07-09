from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.schemas.discovery import DiscoveryContext
from app.services.discovery_mock import get_discovery_context

router = APIRouter(prefix="/api/v1/discovery", tags=["discovery"])


@router.get("/context", response_model=DiscoveryContext)
def discovery_context(user: dict = Depends(get_current_user)):
    clubs, events = get_discovery_context(user["college_id"])
    return {"clubs": clubs, "events": events}
