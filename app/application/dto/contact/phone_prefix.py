from dataclasses import dataclass


@dataclass(frozen=True)
class PhonePrefixOut:
    """DTO carrying phone prefix data of the phone prefix catalogue."""
    id: int
    prefix: str
    country_id: int
