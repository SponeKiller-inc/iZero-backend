from dataclasses import dataclass

from app.application.dto.person.company import CompanyIn
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.natural_person import NaturalPersonIn


@dataclass(frozen=True)
class UserPersonIn:
    """
    Input DTO for AddUserPerson and ChangeUserPerson use-cases; the type of
    the person details says which person type is requested.
    """
    user_id: int
    person: NaturalPersonIn | EntrepreneurIn | CompanyIn
