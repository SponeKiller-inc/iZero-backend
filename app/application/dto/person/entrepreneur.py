from dataclasses import dataclass


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
