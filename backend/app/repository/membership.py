from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Membership, MembershipRole, MembershipStatus, Student, User
from sqlalchemy import select


class MembershipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_membership(self, student_id: int, club_id: int, role: MembershipRole,
                                status: MembershipStatus) -> Membership:
        new_membership = Membership(
            student_id=student_id,
            club_id=club_id,
            role=role,
            status=status,
        )
        self.db.add(new_membership)
        await self.db.flush()
        return new_membership

    async def get(self, student_id: int, club_id: int) -> Membership | None:
        result = await self.db.execute(
            select(Membership).where(
                Membership.student_id == student_id, Membership.club_id == club_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, membership_id: int) -> Membership | None:
        result = await self.db.execute(select(Membership).where(Membership.id == membership_id))
        return result.scalar_one_or_none()

    async def is_leader(self, student_id: int, club_id: int) -> bool:
        result = await self.db.execute(
            select(Membership).where(
                Membership.student_id == student_id,
                Membership.club_id == club_id,
                Membership.role == MembershipRole.LEADER,
                Membership.status == MembershipStatus.APPROVED,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_pending_by_club(self, club_id: int) -> list[tuple[Membership, str]]:
        result = await self.db.execute(
            select(Membership, User.full_name)
            .join(Student, Membership.student_id == Student.id)
            .join(User, Student.user_id == User.id)
            .where(Membership.club_id == club_id, Membership.status == MembershipStatus.PENDING)
            .order_by(Membership.created_at.asc())
        )
        return result.all()

    async def get_members_by_club(self, club_id: int) -> list[tuple[Membership, str]]:
        result = await self.db.execute(
            select(Membership, User.full_name)
            .join(Student, Membership.student_id == Student.id)
            .join(User, Student.user_id == User.id)
            .where(Membership.club_id == club_id, Membership.status == MembershipStatus.APPROVED)
            .order_by(Membership.created_at.asc())
        )
        return result.all()

    async def set_status(self, membership: Membership, status: MembershipStatus) -> Membership:
        membership.status = status
        return membership
