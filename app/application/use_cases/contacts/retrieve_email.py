from app.application.constants.use_case import UseCase
from app.application.dto.contact.email import EmailOut
from app.application.exceptions.contact import EmailValidationError
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.entities.email import Email
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.value_objects.contact import EmailAddress


class RetrieveEmail:

    def __init__(self, email_repository: EmailRepository) -> None:
        """
        Initialize use-case

        Args:
            email_repository: E-mail repository
        """
        self.email_repository = email_repository

    @authorize(EntityType.CONTACTS, UseCase.CONTACTS_RETRIEVE_EMAIL)
    def execute(self, address: str | None) -> EmailOut:
        """
        Retrieve the e-mail with the given address; an e-mail that is not stored yet is
        created, a stored one is never changed

        Args:
            address: E-mail address

        Returns:
            The e-mail

        Raises:
            EmailValidationError: If the address is missing or has invalid format
        """
        if not address:
            raise EmailValidationError("E-mail needs an address")

        try:
            email_address = EmailAddress(address)
        except ValueError as e:
            raise EmailValidationError(str(e)) from e

        email = self.email_repository.get_by_address(email_address.value)

        if email is None:
            email = self.email_repository.save(Email.create(address=email_address))

        return EmailOut(id=email.id, address=email.address.value)
