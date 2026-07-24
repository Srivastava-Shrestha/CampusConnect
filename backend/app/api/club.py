from fastapi import APIRouter, Depends, Query, Security
from app.schemas import (
    CreateClubRequest, UpdateClubRequest, CreateClubResponse, ClubStatusResponse,
    ClubListItem, ClubDetailResponse, JoinResponse, RequestActionRequest, RequestActionResponse,
    PendingRequestItem, MemberItem
)
from app.services import ClubService, MembershipService
from app.core.di import get_club_service, get_membership_service, get_user_info
from app.models import ClubStatus, ClubType

club_router = APIRouter(prefix="/clubs", tags=["Clubs"])


@club_router.post("", response_model=CreateClubResponse)
async def create_club(
    data: CreateClubRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.create(payload, data)


@club_router.get("", response_model=list[ClubListItem])
async def browse_clubs(
    status: ClubStatus | None = Query(None, description="Admins only; students always get ACTIVE clubs"),
    type: ClubType | None = Query(None),
    category: str | None = Query(None, min_length=1, max_length=50),
    search: str | None = Query(None, min_length=1, max_length=100, description="Matches name, description or category"),
    payload: dict = Security(get_user_info, scopes=["STUDENT", "CAMPUS_ADMIN"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.list(payload, status=status, search=search, category=category, type=type)


@club_router.get("/{club_id}", response_model=ClubDetailResponse)
async def view_club(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT", "CAMPUS_ADMIN"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.get(payload, club_id)


@club_router.put("/{club_id}", response_model=ClubDetailResponse)
async def edit_club(
    club_id: int,
    data: UpdateClubRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.update(payload, club_id, data)


@club_router.delete("/{club_id}", response_model=ClubStatusResponse)
async def delete_club(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.delete(payload, club_id)


@club_router.patch("/{club_id}/approve", response_model=ClubStatusResponse)
async def approve_club(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["CAMPUS_ADMIN"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.approve(payload, club_id)


@club_router.patch("/{club_id}/reject", response_model=ClubStatusResponse)
async def reject_club(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["CAMPUS_ADMIN"]),
    service: ClubService = Depends(get_club_service),
):
    return await service.reject(payload, club_id)


@club_router.post("/{club_id}/join", response_model=JoinResponse)
async def join_club(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: MembershipService = Depends(get_membership_service),
):
    return await service.join(payload, club_id)


@club_router.get("/{club_id}/requests", response_model=list[PendingRequestItem])
async def pending_requests(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: MembershipService = Depends(get_membership_service),
):
    return await service.pending_requests(payload, club_id)


@club_router.patch("/{club_id}/requests/{membership_id}", response_model=RequestActionResponse)
async def handle_request(
    club_id: int,
    membership_id: int,
    data: RequestActionRequest,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: MembershipService = Depends(get_membership_service),
):
    return await service.handle_request(payload, club_id, membership_id, data)


@club_router.get("/{club_id}/members", response_model=list[MemberItem])
async def club_members(
    club_id: int,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: MembershipService = Depends(get_membership_service),
):
    return await service.members(club_id)
