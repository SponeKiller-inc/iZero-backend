from dataclasses import dataclass
from datetime import datetime

@dataclass
class LoginLocalIn:
    """
    Input DTO for LoginLocal use-case
    """
    email: str
    password: str
    session_id: int

@dataclass
class LoginLocalOut:
    """
    Output DTO for LoginLocal use-case
    """
    access_token: str
    access_token_type: str
    refresh_token: str
    refresh_token_expires_at: datetime
    csrf_token: str
