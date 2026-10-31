from app.application.constants.use_case import UseCase
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import PersonValidationError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.application.use_cases.contacts.retrieve_email import RetrieveEmail
from app.application.use_cases.contacts.retrieve_phone import RetrievePhone
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
from app.domain.shared.repositories.title import TitleRepository


class AddNaturalPerson:

    def __init__(
        self,
        person_repository: PersonRepository,
        natural_person_repository: NaturalPersonRepository,
        title_repository: TitleRepository,
        person_title_repository: PersonTitleRepository,
        time_provider: TimeProvider,
        retrieve_phone: RetrievePhone,
        retrieve_email: RetrieveEmail,
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
            retrieve_phone: Retrieve phone use-case
            retrieve_email: Retrieve e-mail use-case
            retrieve_person: Retrieve person use-case
        """
        self.person_repository = person_repository
        self.natural_person_repository = natural_person_repository
        self.title_repository = title_repository
        self.person_title_repository = person_title_repository
        self.time_provider = time_provider
        self.retrieve_phone = retrieve_phone
        self.retrieve_email = retrieve_email
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
            PhoneValidationError: If the phone is incomplete, its calling code does not exist
                or the number has invalid format
            EmailValidationError: If the e-mail address has invalid format
            PersonValidationError: If a name is empty, the person is younger than 18 or
                a title does not exist
        """
        titles = self.title_repository.get(dto.title_ids)

        if len(titles) != len(set(dto.title_ids)):
            raise PersonValidationError("Some of the titles do not exist")

        phone = (
            self.retrieve_phone.execute(dto.phone_prefix_id, dto.phone_number)
            if dto.phone_prefix_id is not None or dto.phone_number
            else None
        )
        email = self.retrieve_email.execute(dto.email) if dto.email else None

        person = self.person_repository.save(Person.create(PersonType.NATURAL_PERSON))
        now = self.time_provider.now()

        try:
            natural_person = NaturalPerson.create(
                person=person,
                first_name=dto.first_name,
                last_name=dto.last_name,
                date_of_birth=dto.date_of_birth,
                phone_id=phone.id if phone else None,
                email_id=email.id if email else None,
                current_time=now,
            )
            person_titles = [PersonTitle.assign(person, title, now) for title in titles]
        except (ValueError, person_errors.PersonValidationError) as e:
            raise PersonValidationError(str(e)) from e

        self.natural_person_repository.save(natural_person)

        for person_title in person_titles:
            self.person_title_repository.save(person_title)

        return self.retrieve_person.execute(person.id)
