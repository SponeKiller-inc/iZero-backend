from pydantic import BaseModel

from app.infrastructure.api.schemas.person.company import CompanySchemaIn
from app.infrastructure.api.schemas.person.entrepreneur import EntrepreneurSchemaIn
from app.infrastructure.api.schemas.person.natural_person import NaturalPersonSchemaIn
from app.infrastructure.api.schemas.person.person import PersonSchemaOut


class UserPersonSchemaIn(BaseModel):
    """Schema carrying the user's person; the type of the details says which
    person type is requested."""

    person: NaturalPersonSchemaIn | EntrepreneurSchemaIn | CompanySchemaIn


class UserPersonSchemaOut(PersonSchemaOut):
    """Schema carrying the user's person."""
