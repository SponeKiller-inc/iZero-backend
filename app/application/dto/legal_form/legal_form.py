from dataclasses import dataclass


@dataclass(frozen=True)
class LegalFormOut:
    """DTO carrying legal form data of the legal form catalogue."""
    id: int
    code: str
    name: str
