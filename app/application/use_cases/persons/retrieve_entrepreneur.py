from app.application.constants.use_case import UseCase
from app.application.dto.person.entrepreneur import EntrepreneurOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.security.authorize import authorize
from app.domain.persons.repositories.entrepreneur import EntrepreneurRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository


class RetrieveEntrepreneur:

    def __init__(
        self,
        entrepreneur_repository: EntrepreneurRepository,
        phone_repository: PhoneRepository,
        phone_prefix_repository: PhonePrefixRepository,
        email_repository: EmailRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            entrepreneur_repository: Entrepreneur repository
            phone_repository: Phone repository
            phone_prefix_repository: Phone prefix repository
            email_repository: E-mail repository
        """
        self.entrepreneur_repository = entrepreneur_repository
        self.phone_repository = phone_repository
        self.phone_prefix_repository = phone_prefix_repository
        self.email_repository = email_repository

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE)
    def execute(self, person_id: int) -> EntrepreneurOut:
        """
        Retrieve the details of an entrepreneur with their contacts

        Args:
            person_id: Person ID

        Returns:
            The entrepreneur details

        Raises:
            PersonNotFoundError: If the entrepreneur details do not exist
        """
        entrepreneur = self.entrepreneur_repository.get_by_person_id(person_id)

        if entrepreneur is None:
            raise PersonNotFoundError("Entrepreneur details do not exist")

        phone = self.phone_repository.get(entrepreneur.phone_id) if entrepreneur.phone_id is not None else None
        phone_prefix = self.phone_prefix_repository.get(phone.phone_prefix_id) if phone else None
        email = self.email_repository.get(entrepreneur.email_id) if entrepreneur.email_id is not None else None

        return EntrepreneurOut(
            name=entrepreneur.name,
            registration_number=entrepreneur.registration_number.value,
            vat_number=entrepreneur.vat_number.value if entrepreneur.vat_number else None,
            is_vat_payer=entrepreneur.is_vat_payer,
            phone_prefix_id=phone_prefix.id if phone_prefix else None,
            phone_prefix=phone_prefix.prefix if phone_prefix else None,
            phone_number=phone.number.value if phone else None,
            email=email.address.value if email else None,
        )
