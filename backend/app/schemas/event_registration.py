from datetime import datetime
from pydantic import BaseModel, model_validator
from app.models import EventStatus, RegistrationResult


class RegistrationConfirmation(BaseModel):
    registration_id: int
    event_id: int
    event_title: str
    venue: str
    starts_at: datetime
    message: str


class UnregisterResponse(BaseModel):
    event_id: int
    message: str


class ParticipantItem(BaseModel):
    registration_id: int
    student_id: int
    full_name: str
    email: str
    roll_no: str | None
    branch: str | None
    year: int | None
    checked_in: bool
    checked_in_at: datetime | None
    result: RegistrationResult
    registered_at: datetime


class MarkAttendanceRequest(BaseModel):
    checked_in: bool


class AttendanceResponse(BaseModel):
    registration_id: int
    student_id: int
    full_name: str
    checked_in: bool
    checked_in_at: datetime | None
    message: str


class SetResultRequest(BaseModel):
    result: RegistrationResult

    @model_validator(mode="after")
    def valid_result(self):
        if self.result == RegistrationResult.REGISTRANT:
            raise ValueError("result must be WINNER, RUNNER_UP or PARTICIPANT")
        return self


class ResultResponse(BaseModel):
    registration_id: int
    student_id: int
    full_name: str
    result: RegistrationResult
    message: str


class MyRegistrationItem(BaseModel):
    registration_id: int
    event_id: int
    event_title: str
    club_id: int
    club_name: str
    venue: str
    starts_at: datetime
    ends_at: datetime
    event_status: EventStatus
    checked_in: bool
    result: RegistrationResult


class MyResultItem(BaseModel):
    event_id: int
    event_title: str
    club_id: int
    club_name: str
    venue: str
    starts_at: datetime
    registration_id: int
    result: RegistrationResult
