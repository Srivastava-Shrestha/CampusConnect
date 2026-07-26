from app.exceptions.base import AppException
from app.exceptions.user import (
    UserAlreadyExistError, CollegeNotFoundError, AuthenticationError,
    CollegeAlreadyExistError, IncorrectCredentialError, AuthorizationError
)
from app.exceptions.club import (
    ClubNotFoundError, ClubNotActiveError, NotClubLeaderError, AlreadyMemberError,
    MembershipNotFoundError, ClubActionNotAllowedError, StudentNotFoundError
)
from app.exceptions.event import (
    EventNotFoundError, EventActionNotAllowedError, EventNotPublishedError, EventFullError,
    RegistrationClosedError, AlreadyRegisteredError, RegistrationNotFoundError,
    NotClubMemberError, AttendanceNotAllowedError, NotCheckedInError
)