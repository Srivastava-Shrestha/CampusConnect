from datetime import datetime
from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base

class College(Base):
    __tablename__ = "colleges"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email_suffix: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped[list["User"]] = relationship(back_populates="college")