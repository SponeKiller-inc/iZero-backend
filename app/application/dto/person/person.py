from dataclasses import dataclass

from app.application.dto.person.company import CompanyOut
from app.application.dto.person.entrepreneur import EntrepreneurOut
from app.application.dto.person.natural_person import NaturalPersonOut


@dataclass(frozen=True)
class PersonOut:
    """DTO carrying a person with the details of its type; details of the other types are None."""
    id: int
    person_type: str
    natural_person: NaturalPersonOut | None = None
    entrepreneur: EntrepreneurOut | None = None
    company: CompanyOut | None = None
