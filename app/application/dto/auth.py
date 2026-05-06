from dataclasses import dataclass

@dataclass(frozen=True)
class RegistrationInfo:
    """DTO carrying user data from any identity provider."""
    user_id: str
    email: str