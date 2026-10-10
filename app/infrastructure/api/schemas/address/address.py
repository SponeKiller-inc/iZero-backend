from pydantic import BaseModel, ConfigDict


class AddressSchemaOut(BaseModel):
    """Schema carrying address data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: int
    street: str | None
    building_number: str
    orientation_number: str | None
    orientation_number_letter: str | None
    district: str | None
    city: str
    postal_code: int
    country_id: int
