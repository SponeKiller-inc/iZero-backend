from dataclasses import dataclass

from app.application.dto.person.natural_person import (
    NaturalPersonIn,
    NaturalPersonOut,
)
from app.application.dto.person.person_address import AddressIn, PersonAddressOut


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
    addresses: list[AddressIn]

@dataclass(frozen=True)
class CompanyOut:
    """DTO carrying company details."""
    name: str
    legal_form_id: int
    legal_form: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative: NaturalPersonOut
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
    addresses: list[PersonAddressOut]
