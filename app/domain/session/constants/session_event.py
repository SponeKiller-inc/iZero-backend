from enum import StrEnum

class SessionEventType(StrEnum):
    INITIALIZED = "session_initialized"
    USER_LOGGED_IN        = "user_logged_in"
    USER_LOGGED_OUT       = "user_logged_out"
    SESSION_EXPIRED       = "session_expired"