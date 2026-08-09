from datetime import datetime
from sqlalchemy import ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base, utcnow
from app.models.event_registration import RegistrationResult


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_id: Mapped[int] = mapped_column(ForeignKey("event_registrations.id"), unique=True)
    serial: Mapped[str] = mapped_column(unique=True, index=True)
    result: Mapped[RegistrationResult] = mapped_column(Enum(RegistrationResult))
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                default=utcnow,
                                                server_default=func.now())

    registration: Mapped["EventRegistration"] = relationship(back_populates="certificate")
