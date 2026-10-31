from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyIn:
    """
    Input DTO for AddCompany and ChangeCompany use-cases.
    """
    name: str
    legal_form_id: int
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative_person_id: int
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None
