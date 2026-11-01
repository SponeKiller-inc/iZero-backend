from app.application.constants.use_case import UseCase
from app.application.dto.person.person_address import PersonAddressOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.application.use_cases.addresses.retrieve_address import RetrieveAddress
from app.domain.addresses.constants.address_type import (
    ADDRESS_TYPE_MAILING_TYPE,
    ADDRESS_TYPE_PERMANENT_TYPE,
)
from app.domain.addresses.repositories.address_type import AddressTypeRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.persons.repositories.person_address import PersonAddressRepository
from app.domain.shared.constants.entity_type import EntityType


class RetrievePersonAddresses:

    def __init__(
        self,
        person_repository: PersonRepository,
        person_address_repository: PersonAddressRepository,
        address_type_repository: AddressTypeRepository,
        time_provider: TimeProvider,
        retrieve_address: RetrieveAddress,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            person_address_repository: Person address repository
            address_type_repository: Address type repository
            time_provider: Time provider
            retrieve_address: Retrieve address use-case
        """
        self.person_repository = person_repository
        self.person_address_repository = person_address_repository
        self.address_type_repository = address_type_repository
        self.time_provider = time_provider
        self.retrieve_address = retrieve_address

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE_ADDRESS)
    def execute(self, person_id: int) -> list[PersonAddressOut]:
        """
        Retrieve the addresses currently assigned to a person

        Args:
            person_id: Person ID

        Returns:
            The current addresses of the person, empty if the person has no address

        Raises:
            PersonNotFoundError: If the person does not exist
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        person_addresses = self.person_address_repository.get(person_id, self.time_provider.now())
        address_types = {
            address_type.id: address_type.type
            for address_type in (
                self.address_type_repository.get_by_type(ADDRESS_TYPE_PERMANENT_TYPE),
                self.address_type_repository.get_by_type(ADDRESS_TYPE_MAILING_TYPE),
            )
        }

        return [
            PersonAddressOut(
                id=person_address.id,
                address_type=address_types[person_address.address_type_id],
                address=self.retrieve_address.execute(person_address.address_id),
            )
            for person_address in person_addresses
        ]
