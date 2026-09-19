from datetime import datetime

from pydantic import BaseModel


class ModuleGroupIn(BaseModel):
    """Schema carrying data to create a module group."""

    name: str
    valid_from: datetime


class ModuleGroupOut(BaseModel):
    """Schema carrying created module group data."""

    id: int
    name: str
    valid_from: datetime
    valid_to: datetime
