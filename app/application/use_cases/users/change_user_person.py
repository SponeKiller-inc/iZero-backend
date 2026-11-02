from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyIn
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person import PersonOut
from app.application.dto.user.user_person import UserPersonIn
from app.application.exceptions.person import PersonNotFoundError
from app.application.security.authorize import authorize
from app.application.use_cases.persons.change_company import ChangeCompany
from app.application.use_cases.persons.change_entrepreneur import ChangeEntrepreneur
from app.application.use_cases.persons.change_natural_person import ChangeNaturalPerson
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.repositories.user_person import UserPersonRepository


class ChangeUserPerson:

    def __init__(
        self,
        user_person_repository: UserPersonRepository,
        change_natural_person: ChangeNaturalPerson,
        change_entrepreneur: ChangeEntrepreneur,
        change_company: ChangeCompany,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_person_repository: User person repository
            change_natural_person: Change natural person use-case
            change_entrepreneur: Change entrepreneur use-case
            change_company: Change company use-case
        """
        self.user_person_repository = user_person_repository
        self.change_natural_person = change_natural_person
        self.change_entrepreneur = change_entrepreneur
        self.change_company = change_company

    @authorize(EntityType.PERSONS, UseCase.PERSONS_CHANGE_USER_PERSON)
    def execute(self, dto: UserPersonIn) -> PersonOut:
        """
        Change person details of the user

        Args:
            dto: DTO carrying user id and changed person details

        Returns:
            The changed person with the details of its type

        Raises:
            PersonNotFoundError: If user has no person
            PersonTypeChangeNotAllowedError: If the details belong to another person type
            PhoneValidationError: If a phone is incomplete, its calling code does not exist
                or the number has invalid format
            EmailValidationError: If an e-mail address has invalid format
            PersonValidationError: If person details violate the rules of the person type
        """
        user_person = self.user_person_repository.get_by_user_id(dto.user_id)

        if user_person is None:
            raise PersonNotFoundError("User has no person")

        match dto.person:
            case NaturalPersonIn():
                return self.change_natural_person.execute(user_person.person_id, dto.person)
            case EntrepreneurIn():
                return self.change_entrepreneur.execute(user_person.person_id, dto.person)
            case CompanyIn():
                return self.change_company.execute(user_person.person_id, dto.person)
