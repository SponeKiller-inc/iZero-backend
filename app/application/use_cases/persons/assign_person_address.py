from app.application.constants.use_case import UseCase
from app.application.dto.person.person_address import PersonAddressIn, PersonAddressOut
from app.application.exceptions.address import (
    AddressNotFoundError,
    AddressTypeNotFoundError,
)
from app.application.exceptions.person import PersonNotFoundError, PersonValidationError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.application.use_cases.persons.retrieve_person_addresses import (
    RetrievePersonAddresses,
)
from app.domain.addresses.repositories.address import AddressRepository
from app.domain.addresses.repositories.address_type import AddressTypeRepository
from app.domain.persons.entities.person_address import PersonAddress
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.person import PersonRepository
from app.domain.persons.repositories.person_address import PersonAddressRepository
from app.domain.shared.constants.entity_type import EntityType


class AssignPersonAddress:

    def __init__(
        self,
        person_repository: PersonRepository,
        person_address_repository: PersonAddressRepository,
        address_repository: AddressRepository,
        address_type_repository: AddressTypeRepository,
        time_provider: TimeProvider,
        retrieve_person_addresses: RetrievePersonAddresses,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            person_address_repository: Person address repository
            address_repository: Address repository
            address_type_repository: Address type repository
            time_provider: Time provider
            retrieve_person_addresses: Retrieve person addresses use-case
        """
        self.person_repository = person_repository
        self.person_address_repository = person_address_repository
        self.address_repository = address_repository
        self.address_type_repository = address_type_repository
        self.time_provider = time_provider
        self.retrieve_person_addresses = retrieve_person_addresses

    @authorize(EntityType.PERSONS, UseCase.PERSONS_ASSIGN_ADDRESS)
    def execute(self, person_id: int, dto: PersonAddressIn) -> list[PersonAddressOut]:
        """
        Assign an address of the given type to a person; the address the person had
        of that type so far is ended and kept in history

        Args:
            person_id: Person ID
            dto: DTO carrying the assigned address and its type

        Returns:
            The current addresses of the person

        Raises:
            PersonNotFoundError: If the person does not exist
            AddressNotFoundError: If the address does not exist
            AddressTypeNotFoundError: If the address type does not exist
            PersonValidationError: If the current address of the type cannot be ended
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        address = self.address_repository.get(dto.address_id)

        if address is None:
            raise AddressNotFoundError("Address does not exist")

        address_type = self.address_type_repository.get_by_type(dto.address_type)

        if address_type is None:
            raise AddressTypeNotFoundError("Address type does not exist")

        current_person_address = next(
            (
                person_address
                for person_address in self.person_address_repository.get(person_id, self.time_provider.now())
                if person_address.address_type_id == address_type.id
            ),
            None,
        )

        try:
            if current_person_address is not None:
                current_person_address.end(self.time_provider.now())

            assigned_person_address = PersonAddress.assign(person, address, address_type, self.time_provider.now())
        except (ValueError, person_errors.PersonValidationError) as e:
            raise PersonValidationError(str(e)) from e

        if current_person_address is not None:
            self.person_address_repository.save(current_person_address)

        self.person_address_repository.save(assigned_person_address)

        return self.retrieve_person_addresses.execute(person_id)
