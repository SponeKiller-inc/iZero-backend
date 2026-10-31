from app.application.constants.use_case import UseCase
from app.application.dto.contact.phone import PhoneOut
from app.application.exceptions.contact import PhoneValidationError
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.entities.phone import Phone
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.value_objects.contact import PhoneNumber


class RetrievePhone:

    def __init__(
        self,
        phone_prefix_repository: PhonePrefixRepository,
        phone_repository: PhoneRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            phone_prefix_repository: Phone prefix repository
            phone_repository: Phone repository
        """
        self.phone_prefix_repository = phone_prefix_repository
        self.phone_repository = phone_repository

    @authorize(EntityType.CONTACTS, UseCase.CONTACTS_RETRIEVE_PHONE)
    def execute(self, phone_prefix_id: int | None, phone_number: str | None) -> PhoneOut:
        """
        Retrieve the phone with the given calling code and national number; a phone that
        is not stored yet is created, a stored one is never changed

        Args:
            phone_prefix_id: ID of the calling code from the catalogue
            phone_number: National phone number

        Returns:
            The phone

        Raises:
            PhoneValidationError: If the calling code or the number is missing, the
                calling code does not exist or the number is not a Czech 9-digit number
        """
        if phone_prefix_id is None or not phone_number:
            raise PhoneValidationError("Phone needs both a calling code and a number")

        phone_prefix = self.phone_prefix_repository.get(phone_prefix_id)

        if phone_prefix is None:
            raise PhoneValidationError("Phone prefix does not exist")

        try:
            number = PhoneNumber(phone_number)
        except ValueError as e:
            raise PhoneValidationError(str(e)) from e

        phone = self.phone_repository.get_by_number(phone_prefix.id, number.value)

        if phone is None:
            phone = self.phone_repository.save(Phone.create(prefix=phone_prefix, number=number))

        return PhoneOut(
            id=phone.id,
            phone_prefix_id=phone_prefix.id,
            phone_prefix=phone_prefix.prefix,
            number=phone.number.value,
        )
