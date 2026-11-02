from datetime import date

from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.person.person_address import (
    AddressSchemaIn,
    PersonAddressSchemaOut,
)


class NaturalPersonSchemaIn(BaseModel):
    """Schema carrying natural person details, also used for the representative
    of a company."""

    first_name: str
    last_name: str
    date_of_birth: date
    title_ids: list[int]
    phone_prefix_id: int | None
    phone_number: str | None
    email: str | None
    addresses: list[AddressSchemaIn]


class NaturalPersonSchemaOut(BaseModel):
    """Schema carrying natural person details; titles are ordered as written
    next to the name."""

    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    date_of_birth: date
    prefix_titles: list[str]
    suffix_titles: list[str]
    phone_prefix_id: int | None
    phone_prefix: str | None
    phone_number: str | None
    email: str | None
    addresses: list[PersonAddressSchemaOut]
