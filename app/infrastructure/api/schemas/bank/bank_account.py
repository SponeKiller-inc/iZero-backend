from pydantic import BaseModel, ConfigDict


class BankSchemaOut(BaseModel):
    """Schema carrying bank data of the bank catalogue."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address_id: int
    code: str
    swift: str

