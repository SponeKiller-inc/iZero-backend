from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class NaturalPersonIn:
    """
    Input DTO for AddNaturalPerson and ChangeNaturalPerson use-cases.
    """
    first_name: str
    last_name: str
    date_of_birth: date
    title_ids: list[int]
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None

@dataclass(frozen=True)
class NaturalPersonOut:
    """DTO carrying natural person details; titles are ordered as written next to the name."""
    first_name: str
    last_name: str
    date_of_birth: date
    prefix_titles: list[str]
    suffix_titles: list[str]
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
