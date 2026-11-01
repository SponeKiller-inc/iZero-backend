from pydantic import BaseModel, ConfigDict


class LegalFormSchemaOut(BaseModel):
    """Schema carrying legal form data of the legal form catalogue."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
