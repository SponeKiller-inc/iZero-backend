from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.address.address import AddressSchemaOut


class AddressSchemaIn(BaseModel):
    """Schema carrying one address of a person with its type."""

    address_id: int
    address_type_id: int


class PersonAddressSchemaOut(BaseModel):
    """Schema carrying an address currently assigned to a person with its
    type."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    address_type: str
    address: AddressSchemaOut
