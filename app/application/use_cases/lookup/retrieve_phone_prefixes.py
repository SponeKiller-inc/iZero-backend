from app.application.constants.use_case import UseCase
from app.application.dto.contact.phone_prefix import PhonePrefixOut
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository


class RetrievePhonePrefixes:

    def __init__(self, phone_prefix_repository: PhonePrefixRepository) -> None:
        """
        Initialize use-case

        Args:
            phone_prefix_repository: Phone prefix repository
        """
        self.phone_prefix_repository = phone_prefix_repository

    @authorize(EntityType.CONTACTS, UseCase.CONTACTS_RETRIEVE_PHONE_PREFIXES)
    def execute(self) -> list[PhonePrefixOut]:
        """
        Retrieve all phone prefixes of the catalogue

        Returns:
            List of all phone prefixes, empty if the catalogue is empty
        """
        return [
            PhonePrefixOut(
                id=phone_prefix.id,
                prefix=phone_prefix.prefix,
                country_id=phone_prefix.country_id,
            )
            for phone_prefix in self.phone_prefix_repository.get_all()
        ]
