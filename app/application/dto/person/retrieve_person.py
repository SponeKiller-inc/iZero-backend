from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RetrieveNaturalPersonOut:
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

@dataclass(frozen=True)
class RetrieveEntrepreneurOut:
    """DTO carrying entrepreneur details."""
    name: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None

@dataclass(frozen=True)
class RetrieveCompanyOut:
    """DTO carrying company details."""
    name: str
    legal_form_id: int
    legal_form: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative_person_id: int
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None

@dataclass(frozen=True)
class RetrievePersonOut:
    """DTO carrying a person with the details of its type; details of the other types are None."""
    id: int
    person_type: str
    natural_person: RetrieveNaturalPersonOut | None = None
    entrepreneur: RetrieveEntrepreneurOut | None = None
    company: RetrieveCompanyOut | None = None
