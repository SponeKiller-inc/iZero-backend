from dataclasses import dataclass

from app.application.dto.person.person_address import AddressIn, PersonAddressOut


@dataclass(frozen=True)
class EntrepreneurIn:
    """
    Input DTO for AddEntrepreneur and ChangeEntrepreneur use-cases.
    """
    name: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None
    addresses: list[AddressIn]

@dataclass(frozen=True)
class EntrepreneurOut:
    """DTO carrying entrepreneur details."""
    name: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
    addresses: list[PersonAddressOut]
