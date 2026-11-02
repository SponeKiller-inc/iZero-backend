from pydantic import BaseModel, ConfigDict


class TitleSchemaOut(BaseModel):
    """Schema carrying title data of the title catalogue."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title_type: str
    name: str
