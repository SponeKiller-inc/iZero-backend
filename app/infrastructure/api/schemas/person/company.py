from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.person.natural_person import (
    NaturalPersonSchemaIn,
    NaturalPersonSchemaOut,
)
from app.infrastructure.api.schemas.person.person_address import (
    AddressSchemaIn,
    PersonAddressSchemaOut,
)


class CompanySchemaIn(BaseModel):
    """Schema carrying company details together with its representative."""

    name: str
    legal_form_id: int
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative: NaturalPersonSchemaIn
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None
    addresses: list[AddressSchemaIn]


class CompanySchemaOut(BaseModel):
    """Schema carrying company details together with its representative."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    legal_form_id: int
    legal_form: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    representative: NaturalPersonSchemaOut
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
    addresses: list[PersonAddressSchemaOut]
