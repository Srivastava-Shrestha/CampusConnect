import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base, utcnow


class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    CAMPUS_ADMIN = "CAMPUS_ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    college_id: Mapped[int | None] = mapped_column(ForeignKey("colleges.id"))
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    profile_image_url: Mapped[str | None] = mapped_column()
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=utcnow,
                                                 server_default=func.now())

    college: Mapped["College"] = relationship(back_populates="users")
    student: Mapped["Student | None"] = relationship(back_populates="user", uselist=False)
    campus_admin: Mapped["CampusAdmin | None"] = relationship(back_populates="user", uselist=False)





