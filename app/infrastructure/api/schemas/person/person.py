from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.person.company import CompanySchemaOut
from app.infrastructure.api.schemas.person.entrepreneur import EntrepreneurSchemaOut
from app.infrastructure.api.schemas.person.natural_person import NaturalPersonSchemaOut


class PersonSchemaOut(BaseModel):
    """Schema carrying a person with the details of its type; details of the
    other types are None."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    person_type: str
    natural_person: NaturalPersonSchemaOut | None = None
    entrepreneur: EntrepreneurSchemaOut | None = None
    company: CompanySchemaOut | None = None
