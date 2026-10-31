from dataclasses import dataclass


@dataclass(frozen=True)
class PhoneOut:
    """DTO carrying a phone with its calling code."""
    id: int
    phone_prefix_id: int
    phone_prefix: str
    number: str
