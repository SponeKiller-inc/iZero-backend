from app.application.constants.use_case import UseCase
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import (
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.application.use_cases.persons.email import get_or_create_email
from app.application.use_cases.persons.phone import get_or_create_phone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
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


class ChangeNaturalPerson:

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

    @authorize(EntityType.PERSONS, UseCase.PERSONS_CHANGE)
    def execute(self, person_id: int, dto: NaturalPersonIn) -> PersonOut:
        """
        Change details of a natural person

        Args:
            person_id: Person ID
            dto: DTO carrying changed natural person data

        Returns:
            The changed person with its natural person details

        Raises:
            PersonNotFoundError: If the person or its natural person details do not exist
            PersonTypeChangeNotAllowedError: If the person is not a natural person
            PersonValidationError: If the phone is incomplete or its calling code does not
                exist, phone number or e-mail has invalid format, a name is empty,
                the person is younger than 18 or a title does not exist or cannot be assigned
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        if person.person_type != PersonType.NATURAL_PERSON:
            raise PersonTypeChangeNotAllowedError("Person is not a natural person")

        natural_person = self.natural_person_repository.get_by_person_id(person_id)

        if natural_person is None:
            raise PersonNotFoundError("Natural person details do not exist")

        titles = self._get_titles(dto.title_ids)
        phone = get_or_create_phone(
            self.phone_prefix_repository,
            self.phone_repository,
            dto.phone_prefix_id,
            dto.phone_number,
        )
        email = get_or_create_email(self.email_repository, dto.email)

        now = self.time_provider.now()
        current_person_titles = self.person_title_repository.get(person_id, now)
        current_title_ids = {person_title.title_id for person_title in current_person_titles}
        requested_title_ids = {title.id for title in titles}

        try:
            natural_person.update(
                person=person,
                first_name=dto.first_name,
                last_name=dto.last_name,
                date_of_birth=dto.date_of_birth,
                phone=phone,
                email=email,
                current_time=now,
            )

            # Titles the person no longer holds keep their history, the new ones are valid from now on
            ended_person_titles = [
                person_title
                for person_title in current_person_titles
                if person_title.title_id not in requested_title_ids
            ]
            for person_title in ended_person_titles:
                person_title.end(now)

            assigned_person_titles = [
                PersonTitle.assign(person, title, now)
                for title in titles
                if title.id not in current_title_ids
            ]
        except (ValueError, person_errors.PersonValidationError) as e:
            raise PersonValidationError(str(e)) from e

        self.natural_person_repository.save(natural_person)

        for person_title in ended_person_titles + assigned_person_titles:
            self.person_title_repository.save(person_title)

        return self.retrieve_person.execute(person_id)

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
