from app.application.constants.use_case import UseCase
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import PersonValidationError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.application.use_cases.persons.email import get_or_create_email
from app.application.use_cases.persons.phone import get_or_create_phone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.natural_person import NaturalPerson
from app.domain.persons.entities.person import Person
from app.domain.persons.entities.person_title import PersonTitle
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.natural_person import NaturalPersonRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.persons.repositories.person_title import PersonTitleRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.entities.title import Title
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.repositories.title import TitleRepository


class AddNaturalPerson:

    def __init__(
        self,
        person_repository: PersonRepository,
        natural_person_repository: NaturalPersonRepository,
        title_repository: TitleRepository,
        person_title_repository: PersonTitleRepository,
        time_provider: TimeProvider,
        phone_prefix_repository: PhonePrefixRepository,
        phone_repository: PhoneRepository,
        email_repository: EmailRepository,
        retrieve_person: RetrievePerson,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            natural_person_repository: Natural person repository
            title_repository: Title repository
            person_title_repository: Person title repository
            time_provider: Time provider
            phone_prefix_repository: Phone prefix repository
            phone_repository: Phone repository
            email_repository: E-mail repository
            retrieve_person: Retrieve person use-case
        """
        self.person_repository = person_repository
        self.natural_person_repository = natural_person_repository
        self.title_repository = title_repository
        self.person_title_repository = person_title_repository
        self.time_provider = time_provider
        self.phone_prefix_repository = phone_prefix_repository
        self.phone_repository = phone_repository
        self.email_repository = email_repository
        self.retrieve_person = retrieve_person

    @authorize(EntityType.PERSONS, UseCase.PERSONS_ADD)
    def execute(self, dto: NaturalPersonIn) -> PersonOut:
        """
        Add a new natural person

        Args:
            dto: DTO carrying natural person data

        Returns:
            The added person with its natural person details

        Raises:
            PersonValidationError: If the phone is incomplete or its calling code does not
                exist, phone number or e-mail has invalid format, a name is empty,
                the person is younger than 18 or a title does not exist or cannot be assigned
        """
        titles = self._get_titles(dto.title_ids)
        phone = get_or_create_phone(
            self.phone_prefix_repository,
            self.phone_repository,
            dto.phone_prefix_id,
            dto.phone_number,
        )
        email = get_or_create_email(self.email_repository, dto.email)

        person = self.person_repository.save(Person.create(PersonType.NATURAL_PERSON))
        now = self.time_provider.now()

        try:
            natural_person = NaturalPerson.create(
                person=person,
                first_name=dto.first_name,
                last_name=dto.last_name,
                date_of_birth=dto.date_of_birth,
                phone=phone,
                email=email,
                current_time=now,
            )
            person_titles = [PersonTitle.assign(person, title, now) for title in titles]
        except (ValueError, person_errors.PersonValidationError) as e:
            raise PersonValidationError(str(e)) from e

        self.natural_person_repository.save(natural_person)

        for person_title in person_titles:
            self.person_title_repository.save(person_title)

        return self.retrieve_person.execute(person.id)

    def _get_titles(self, title_ids: list[int]) -> list[Title]:
        """
        Load the requested titles in the order they are written next to the name.

        Raises:
            PersonValidationError: If a title does not exist
        """
        titles = self.title_repository.get_many(title_ids)

        if len(titles) != len(set(title_ids)):
            raise PersonValidationError("Some of the titles do not exist")

        return titles
