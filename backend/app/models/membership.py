import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base


class MembershipRole(str, enum.Enum):
    LEADER = "LEADER"
    MEMBER = "MEMBER"


class MembershipStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"))
    role: Mapped[MembershipRole] = mapped_column(Enum(MembershipRole))
    status: Mapped[MembershipStatus] = mapped_column(Enum(MembershipStatus))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    student: Mapped["Student"] = relationship(back_populates="memberships")
    club: Mapped["Club"] = relationship(back_populates="memberships")
