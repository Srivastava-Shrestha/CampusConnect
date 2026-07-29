from fastapi import APIRouter, Depends, Query, Security
from app.schemas import (
    CreateEventRequest, UpdateEventRequest, CreateEventResponse, EventStatusResponse,
    EventListItem, EventDetailResponse, RegistrationConfirmation, UnregisterResponse,
    ParticipantItem, MarkAttendanceRequest, AttendanceResponse, SetResultRequest,
    ResultResponse, MyRegistrationItem, MyResultItem
)
from app.services import EventService, EventRegistrationService
from app.core.di import get_event_service, get_event_registration_service, get_user_info
from app.models import EventStatus

event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.post("", response_model=CreateEventResponse)
async def create_event(
    data: CreateEventRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventService = Depends(get_event_service),
):
    return await service.create(payload, data)


@event_router.get("", response_model=list[EventListItem])
async def browse_events(
    status: EventStatus | None = Query(None, description="Admins only; students always get PUBLISHED events"),
    club_id: int | None = Query(None),
    search: str | None = Query(None, min_length=1, max_length=100, description="Matches title, description or venue"),
    upcoming_only: bool = Query(False, description="Only events that have not finished yet"),
    payload: dict = Security(get_user_info, scopes=["STUDENT", "CAMPUS_ADMIN"]),
    service: EventService = Depends(get_event_service),
):
    return await service.list(payload, status=status, club_id=club_id, search=search,
                              upcoming_only=upcoming_only)


@event_router.get("/me/registrations", response_model=list[MyRegistrationItem])
async def my_registrations(
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.my_registrations(payload)


@event_router.get("/me/results", response_model=list[MyResultItem])
async def my_results(
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.my_results(payload)


@event_router.get("/{event_id}", response_model=EventDetailResponse)
async def view_event(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT", "CAMPUS_ADMIN"]),
    service: EventService = Depends(get_event_service),
):
    return await service.get(payload, event_id)


@event_router.put("/{event_id}", response_model=EventDetailResponse)
async def edit_event(
    event_id: int,
    data: UpdateEventRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventService = Depends(get_event_service),
):
    return await service.update(payload, event_id, data)


@event_router.patch("/{event_id}/publish", response_model=EventStatusResponse)
async def publish_event(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventService = Depends(get_event_service),
):
    return await service.publish(payload, event_id)


@event_router.patch("/{event_id}/cancel", response_model=EventStatusResponse)
async def cancel_event(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventService = Depends(get_event_service),
):
    return await service.cancel(payload, event_id)


@event_router.post("/{event_id}/register", response_model=RegistrationConfirmation)
async def register_for_event(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.register(payload, event_id)


@event_router.delete("/{event_id}/register", response_model=UnregisterResponse)
async def unregister_from_event(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.unregister(payload, event_id)


@event_router.get("/{event_id}/registrations", response_model=list[ParticipantItem])
async def event_participants(
    event_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.participants(payload, event_id)


@event_router.patch("/{event_id}/registrations/{registration_id}/attendance",
                    response_model=AttendanceResponse)
async def mark_attendance(
    event_id: int,
    registration_id: int,
    data: MarkAttendanceRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.mark_attendance(payload, event_id, registration_id, data)


@event_router.patch("/{event_id}/registrations/{registration_id}/result",
                    response_model=ResultResponse)
async def set_result(
    event_id: int,
    registration_id: int,
    data: SetResultRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: EventRegistrationService = Depends(get_event_registration_service),
):
    return await service.set_result(payload, event_id, registration_id, data)
