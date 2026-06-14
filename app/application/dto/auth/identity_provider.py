from dataclasses import dataclass

@dataclass(frozen=True)
class IdentityProviderOut:
    """DTO carrying user data to any identity provider."""
    id: int
    email: str