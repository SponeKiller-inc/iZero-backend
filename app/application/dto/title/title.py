from dataclasses import dataclass


@dataclass(frozen=True)
class TitleOut:
    """DTO carrying title data of the title catalogue."""
    id: int
    title_type: str
    name: str
