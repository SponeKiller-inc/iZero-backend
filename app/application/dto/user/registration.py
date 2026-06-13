from dataclasses import dataclass

@dataclass(frozen=True)
class RegistrationLocalIn:
    """DTO carrying user data from any identity provider."""
    email: str
    password: str

@dataclass(frozen=True)
class RegistrationOauthIn:
    """DTO carrying user data to any identity provider."""
    token: str