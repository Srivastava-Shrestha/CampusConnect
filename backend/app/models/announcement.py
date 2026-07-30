import enum
from datetime import datetime
from sqlalchemy import Text, ForeignKey, Enum, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base


class AnnouncementCategory(str, enum.Enum):
    GENERAL = "GENERAL"
    EVENT_UPDATE = "EVENT_UPDATE"
    RESOURCE = "RESOURCE"
    ACHIEVEMENT = "ACHIEVEMENT"
    URGENT = "URGENT"


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column(Text)
    category: Mapped[AnnouncementCategory] = mapped_column(Enum(AnnouncementCategory))
    is_pinned: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    club: Mapped["Club"] = relationship(back_populates="announcements")
    author: Mapped["Student"] = relationship(back_populates="announcements")
