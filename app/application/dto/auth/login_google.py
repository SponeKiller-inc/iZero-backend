from dataclasses import dataclass
from datetime import datetime


@dataclass
class LoginGoogleIn:
    """
    Input DTO for LoginGoogle use-case
    """
    token: str
    session_id: int

@dataclass
class LoginGoogleOut:
    """
    Output DTO for LoginGoogle use-case
    """
    access_token: str
    access_token_type: str
    refresh_token: str
    refresh_token_expires_at: datetime
    csrf_token: str
