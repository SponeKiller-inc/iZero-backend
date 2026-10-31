from app.application.constants.use_case import UseCase
from app.application.dto.person.natural_person import NaturalPersonOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.domain.persons.repositories.natural_person import NaturalPersonRepository
from app.domain.persons.repositories.person_title import PersonTitleRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.constants.title_type import TITLE_PREFIX_NAME, TITLE_SUFFIX_NAME
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.repositories.title import TitleRepository


class RetrieveNaturalPerson:

    def __init__(
        self,
        natural_person_repository: NaturalPersonRepository,
        title_repository: TitleRepository,
        person_title_repository: PersonTitleRepository,
        phone_repository: PhoneRepository,
        phone_prefix_repository: PhonePrefixRepository,
        email_repository: EmailRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            natural_person_repository: Natural person repository
            title_repository: Title repository
            person_title_repository: Person title repository
            phone_repository: Phone repository
            phone_prefix_repository: Phone prefix repository
            email_repository: E-mail repository
            time_provider: Time provider
        """
        self.natural_person_repository = natural_person_repository
        self.title_repository = title_repository
        self.person_title_repository = person_title_repository
        self.phone_repository = phone_repository
        self.phone_prefix_repository = phone_prefix_repository
        self.email_repository = email_repository
        self.time_provider = time_provider

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE)
    def execute(self, person_id: int) -> NaturalPersonOut:
        """
        Retrieve the details of a natural person with their current titles and contacts

        Args:
            person_id: Person ID

        Returns:
            The natural person details

        Raises:
            PersonNotFoundError: If the natural person details do not exist
        """
        natural_person = self.natural_person_repository.get_by_person_id(person_id)

        if natural_person is None:
            raise PersonNotFoundError("Natural person details do not exist")

        person_titles = self.person_title_repository.get(person_id, self.time_provider.now())
        titles = self.title_repository.get([person_title.title_id for person_title in person_titles])

        phone = self.phone_repository.get(natural_person.phone_id) if natural_person.phone_id is not None else None
        phone_prefix = self.phone_prefix_repository.get(phone.phone_prefix_id) if phone else None
        email = self.email_repository.get(natural_person.email_id) if natural_person.email_id is not None else None

        return NaturalPersonOut(
            first_name=natural_person.first_name,
            last_name=natural_person.last_name,
            date_of_birth=natural_person.date_of_birth,
            prefix_titles=[title.name for title in titles if title.title_type == TITLE_PREFIX_NAME],
            suffix_titles=[title.name for title in titles if title.title_type == TITLE_SUFFIX_NAME],
            phone_prefix_id=phone_prefix.id if phone_prefix else None,
            phone_prefix=phone_prefix.prefix if phone_prefix else None,
            phone_number=phone.number.value if phone else None,
            email=email.address.value if email else None,
        )
