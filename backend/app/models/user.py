import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    CAMPUS_ADMIN = "CAMPUS_ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    college_id: Mapped[int] = mapped_column(ForeignKey("colleges.id"))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    profile_image_url: Mapped[str | None] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    college: Mapped["College"] = relationship(back_populates="users")
    students: Mapped["Student | None"] = relationship(
        back_populates="user", uselist=False
    )
    campus_admin: Mapped["CampusAdmin | None"] = relationship(
        back_populates="user", uselist=False
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    interests: Mapped[str | None] = mapped_column(Text)
    enrollment_no: Mapped[str] = mapped_column(String, nullable=False)
    branch: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="students")


class CampusAdmin(Base):
    __tablename__ = "campus_admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    designation: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(back_populates="campus_admin")