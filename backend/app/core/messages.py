class AuthMessages:
    SIGNUP_SUCCESS = "Account created successfully"
    LOGIN_SUCCESS = "Logged in successfully"


class CollegeMessages:
    ONBOARDED = "College onboarded successfully"


class ClubMessages:
    CREATED_ACTIVE = "Club created and is now live"
    CREATED_PENDING = "Club submitted for admin approval"
    UPDATED = "Club updated successfully"
    ARCHIVED = "Club archived successfully"
    APPROVED = "Club approved"
    REJECTED = "Club rejected"
    STATUS_NEEDS_ROLE = (
        "status must be sent together with role: it means the club status for LEADER "
        "and your membership status for MEMBER"
    )


class MembershipMessages:
    JOIN_REQUESTED = "Join request sent"
    REQUEST_APPROVED = "Join request approved"
    REQUEST_REJECTED = "Join request rejected"


class EventMessages:
    CREATED = "Event created as a draft"
    UPDATED = "Event updated successfully"
    PUBLISHED = "Event published successfully"
    CANCELLED = "Event cancelled successfully"


class RegistrationMessages:
    REGISTERED = "Registered successfully"
    UNREGISTERED = "Registration cancelled"
    CHECKED_IN = "Attendance marked"
    CHECK_IN_UNDONE = "Attendance unmarked"
    RESULT_SET = "Result recorded"
