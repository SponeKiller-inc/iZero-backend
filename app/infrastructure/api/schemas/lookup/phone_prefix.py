from pydantic import BaseModel, ConfigDict


class PhonePrefixSchemaOut(BaseModel):
    """Schema carrying phone prefix data of the phone prefix catalogue."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    prefix: str
    country_id: int
