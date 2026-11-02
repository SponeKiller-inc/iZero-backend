from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.person.person_address import (
    AddressSchemaIn,
    PersonAddressSchemaOut,
)


class EntrepreneurSchemaIn(BaseModel):
    """Schema carrying entrepreneur details."""

    name: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None
    addresses: list[AddressSchemaIn]


class EntrepreneurSchemaOut(BaseModel):
    """Schema carrying entrepreneur details."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    registration_number: str
    vat_number: str | None
    is_vat_payer: bool
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
    addresses: list[PersonAddressSchemaOut]
