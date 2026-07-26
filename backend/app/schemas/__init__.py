from app.schemas.user import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from app.schemas.college import CollegeOnboardingRequest, CollegeOnboardingResponse
from app.schemas.club import (
    ClubLinkSchema, CreateClubRequest, UpdateClubRequest, CreateClubResponse,
    ClubStatusResponse, ClubListItem, ClubDetailResponse, ClubHeadInfo
)
from app.schemas.membership import (
    JoinResponse, RequestActionRequest, RequestActionResponse, PendingRequestItem, MemberItem
)
from app.schemas.event import (
    CreateEventRequest, UpdateEventRequest, CreateEventResponse, EventStatusResponse,
    EventListItem, EventDetailResponse
)
from app.schemas.event_registration import (
    RegistrationConfirmation, UnregisterResponse, ParticipantItem, MarkAttendanceRequest,
    AttendanceResponse, SetResultRequest, ResultResponse, MyRegistrationItem, MyResultItem
)