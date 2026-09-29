from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ModuleSchemaIn(BaseModel):
    """Schema carrying data to create a module."""

    name: str
    module_group_id: int
    valid_from: datetime


class ModuleSchemaOut(BaseModel):
    """Schema carrying created module data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    module_group_id: int
    valid_from: datetime
    valid_to: datetime
