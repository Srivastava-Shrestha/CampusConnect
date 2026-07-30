from app.schemas.user import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from app.schemas.college import CollegeOnboardingRequest, CollegeOnboardingResponse
from app.schemas.club import (
    ClubLinkSchema, CreateClubRequest, UpdateClubRequest, CreateClubResponse,
    ClubStatusResponse, ClubListItem, ClubDetailResponse, ClubHeadInfo, MyClubItem
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
from app.schemas.announcement import (
    CreateAnnouncementRequest, PinAnnouncementRequest, CreateAnnouncementResponse,
    AnnouncementItem, PinAnnouncementResponse, DeleteAnnouncementResponse,
    UnreadCountResponse, MarkAnnouncementsReadResponse
)
from app.schemas.issue import (
    RaiseIssueRequest, ReplyIssueRequest, RaiseIssueResponse, IssueResponseInfo,
    MyIssueItem, LeaderIssueItem, IssueActionResponse, OpenIssueCountResponse
)
from app.schemas.notification import (
    NotificationItem, NotificationCountResponse, NotificationReadResponse,
    MarkAllNotificationsReadResponse
)