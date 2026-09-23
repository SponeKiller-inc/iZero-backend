from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ModuleGroupSchemaIn(BaseModel):
    """Schema carrying data to create a module group."""

    name: str
    valid_from: datetime


class ModuleGroupSchemaOut(BaseModel):
    """Schema carrying created module group data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    valid_from: datetime
    valid_to: datetime
