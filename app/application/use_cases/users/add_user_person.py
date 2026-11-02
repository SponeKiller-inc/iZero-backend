from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyIn
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person import PersonOut
from app.application.dto.user.user_person import UserPersonIn
from app.application.exceptions.person import PersonAlreadyExistsError
from app.application.security.authorize import authorize
from app.application.use_cases.persons.add_company import AddCompany
from app.application.use_cases.persons.add_entrepreneur import AddEntrepreneur
from app.application.use_cases.persons.add_natural_person import AddNaturalPerson
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.entities.user_person import UserPerson
from app.domain.users.repositories.user_person import UserPersonRepository


class AddUserPerson:

    def __init__(
        self,
        user_person_repository: UserPersonRepository,
        add_natural_person: AddNaturalPerson,
        add_entrepreneur: AddEntrepreneur,
        add_company: AddCompany,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_person_repository: User person repository
            add_natural_person: Add natural person use-case
            add_entrepreneur: Add entrepreneur use-case
            add_company: Add company use-case
        """
        self.user_person_repository = user_person_repository
        self.add_natural_person = add_natural_person
        self.add_entrepreneur = add_entrepreneur
        self.add_company = add_company

    @authorize(EntityType.PERSONS, UseCase.PERSONS_ADD_USER_PERSON)
    def execute(self, dto: UserPersonIn) -> PersonOut:
        """
        Add person details of the user

        Args:
            dto: DTO carrying user id and person details of the requested type

        Returns:
            The added person with the details of its type

        Raises:
            PersonAlreadyExistsError: If user already has a person
            PhoneValidationError: If a phone is incomplete, its calling code does not exist
                or the number has invalid format
            EmailValidationError: If an e-mail address has invalid format
            PersonValidationError: If person details violate the rules of the person type
        """
        if self.user_person_repository.get_by_user_id(dto.user_id) is not None:
            raise PersonAlreadyExistsError("User already has a person")

        match dto.person:
            case NaturalPersonIn():
                person = self.add_natural_person.execute(dto.person)
            case EntrepreneurIn():
                person = self.add_entrepreneur.execute(dto.person)
            case CompanyIn():
                person = self.add_company.execute(dto.person)

        user_person = UserPerson.assign(
            user_id=dto.user_id,
            person_id=person.id,
        )

        self.user_person_repository.save(user_person)

        return person
