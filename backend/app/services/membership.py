from app.repository import MembershipRepository, ClubRepository, StudentRepository
from app.models import ClubStatus, MembershipRole, MembershipStatus
from app.schemas import (
    JoinResponse, RequestActionRequest, RequestActionResponse, PendingRequestItem, MemberItem
)
from app.exceptions import (
    ClubNotFoundError, ClubNotActiveError, NotClubLeaderError, AlreadyMemberError,
    MembershipNotFoundError, ClubActionNotAllowedError, StudentNotFoundError
)
from app.core.messages import MembershipMessages


class MembershipService:
    def __init__(self, membership_repo: MembershipRepository, club_repo: ClubRepository,
                 student_repo: StudentRepository):
        self.membership_repo = membership_repo
        self.club_repo = club_repo
        self.student_repo = student_repo

    async def join(self, payload: dict, club_id: int) -> JoinResponse:
        student = await self._get_student(payload)
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise ClubNotFoundError()
        if club.status != ClubStatus.ACTIVE:
            raise ClubNotActiveError()

        existing = await self.membership_repo.get(student.id, club_id)
        if existing:
            raise AlreadyMemberError()

        membership = await self.membership_repo.create_membership(
            student_id=student.id,
            club_id=club_id,
            role=MembershipRole.MEMBER,
            status=MembershipStatus.PENDING,
        )
        return JoinResponse(
            id=membership.id,
            club_id=club_id,
            status=membership.status,
            message=MembershipMessages.JOIN_REQUESTED,
        )

    async def pending_requests(self, payload: dict, club_id: int) -> list[PendingRequestItem]:
        student = await self._get_student(payload)
        await self._assert_leader(student.id, club_id)
        rows = await self.membership_repo.get_pending_by_club(club_id)
        return [
            PendingRequestItem(
                id=membership.id,
                student_id=membership.student_id,
                full_name=full_name,
                role=membership.role,
                status=membership.status,
            )
            for membership, full_name in rows
        ]

    async def handle_request(self, payload: dict, club_id: int, membership_id: int,
                             data: RequestActionRequest) -> RequestActionResponse:
        student = await self._get_student(payload)
        await self._assert_leader(student.id, club_id)

        membership = await self.membership_repo.get_by_id(membership_id)
        if not membership or membership.club_id != club_id:
            raise MembershipNotFoundError()
        if membership.status != MembershipStatus.PENDING:
            raise ClubActionNotAllowedError("Request has already been handled")

        await self.membership_repo.set_status(membership, data.action)
        message = (
            MembershipMessages.REQUEST_APPROVED
            if data.action == MembershipStatus.APPROVED
            else MembershipMessages.REQUEST_REJECTED
        )
        return RequestActionResponse(
            id=membership.id,
            student_id=membership.student_id,
            club_id=membership.club_id,
            status=membership.status,
            message=message,
        )

    async def members(self, club_id: int) -> list[MemberItem]:
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise ClubNotFoundError()
        rows = await self.membership_repo.get_members_by_club(club_id)
        return [
            MemberItem(
                id=membership.id,
                student_id=membership.student_id,
                full_name=full_name,
                role=membership.role,
            )
            for membership, full_name in rows
        ]

    async def _get_student(self, payload: dict):
        student = await self.student_repo.get_student_by_user_id(int(payload.get("sub")))
        if not student:
            raise StudentNotFoundError()
        return student

    async def _assert_leader(self, student_id: int, club_id: int):
        if not await self.membership_repo.is_leader(student_id, club_id):
            raise NotClubLeaderError()
