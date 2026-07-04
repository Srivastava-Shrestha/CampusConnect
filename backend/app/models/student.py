from datetime import datetime
from sqlalchemy import Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base




class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str | None] = mapped_column(Text)
    roll_no: Mapped[str] = mapped_column()
    branch: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="student")