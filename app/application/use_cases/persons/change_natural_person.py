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
from app.application.use_cases.contacts.retrieve_email import RetrieveEmail
from app.application.use_cases.contacts.retrieve_phone import RetrievePhone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person_title import PersonTitle
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.natural_person import NaturalPersonRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.persons.repositories.person_title import PersonTitleRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.title import TitleRepository


class ChangeNaturalPerson:

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
            PhoneValidationError: If the phone is incomplete, its calling code does not exist
                or the number has invalid format
            EmailValidationError: If the e-mail address has invalid format
            PersonValidationError: If a name is empty, the person is younger than 18 or
                a title does not exist
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        if person.person_type != PersonType.NATURAL_PERSON:
            raise PersonTypeChangeNotAllowedError("Person is not a natural person")

        natural_person = self.natural_person_repository.get_by_person_id(person_id)

        if natural_person is None:
            raise PersonNotFoundError("Natural person details do not exist")

        titles = self.title_repository.get_many(dto.title_ids)

        if len(titles) != len(set(dto.title_ids)):
            raise PersonValidationError("Some of the titles do not exist")

        phone = (
            self.retrieve_phone.execute(dto.phone_prefix_id, dto.phone_number)
            if dto.phone_prefix_id is not None or dto.phone_number
            else None
        )
        email = self.retrieve_email.execute(dto.email) if dto.email else None

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
                phone_id=phone.id if phone else None,
                email_id=email.id if email else None,
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
