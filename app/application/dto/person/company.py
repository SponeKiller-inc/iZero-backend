from dataclasses import dataclass

from app.application.dto.person.natural_person import NaturalPersonIn


@dataclass(frozen=True)
class CompanyIn:
    """
    Input DTO for AddCompany and ChangeCompany use-cases; the representative is created
    together with the company and changed together with it.
    """
    name: str
    legal_form_id: int
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative: NaturalPersonIn
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None

@dataclass(frozen=True)
class CompanyOut:
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
