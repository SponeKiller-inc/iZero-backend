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
    def execute(self, dto: PersonAddressIn) -> list[PersonAddressOut]:
        """
        Assign addresses of the given types to a person; the address the
        person had of a type so far is ended and kept in history

        Args:
            dto: DTO carrying the person and the assigned addresses with their
                types

        Returns:
            The current addresses of the person

        Raises:
            PersonNotFoundError: If the person does not exist
            AddressNotFoundError: If an address does not exist
            AddressTypeNotFoundError: If an address type does not exist
            PersonValidationError: If the current address of a type cannot be
                ended
        """
        person = self.person_repository.get(dto.person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        for assigned_address in dto.addresses:
            address = self.address_repository.get(assigned_address.address_id)

            if address is None:
                raise AddressNotFoundError("Address does not exist")

            address_type = self.address_type_repository.get(
                assigned_address.address_type_id
            )

            if address_type is None:
                raise AddressTypeNotFoundError("Address type does not exist")

            current_person_address = next(
                (
                    person_address
                    for person_address in self.person_address_repository.get(
                        dto.person_id, self.time_provider.now()
                    )
                    if person_address.address_type_id == address_type.id
                ),
                None,
            )

            # The same address of the same type is already assigned, nothing
            # changes
            if (
                current_person_address is not None
                and current_person_address.address_id == address.id
            ):
                continue

            try:
                if current_person_address is not None:
                    current_person_address.end(self.time_provider.now())

                # Validity is inclusive on both ends, the new address starts
                # later so that the two never overlap
                assigned_person_address = PersonAddress.assign(
                    person,
                    address,
                    address_type,
                    self.time_provider.shifted_now(),
                )
            except (ValueError, person_errors.PersonValidationError) as e:
                raise PersonValidationError(str(e)) from e

            if current_person_address is not None:
                self.person_address_repository.save(current_person_address)

            self.person_address_repository.save(assigned_person_address)

        return self.retrieve_person_addresses.execute(dto.person_id)
