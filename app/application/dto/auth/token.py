from dataclasses import dataclass
from datetime import datetime

from app.domain.users.constants.registration_source_type import RegistrationSourceType


@dataclass
class TokenPayload:
    """DTO carrying access token payload"""
    user_id: int
    provider: RegistrationSourceType
    expired_at: datetime