from datetime import datetime
from typing import Self

from app.domain.addresses.entities.address import Address
from app.domain.addresses.entities.address_type import AddressType
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions.person import PersonValidationError
from app.domain.shared.value_objects.period import ValidityPeriod


class PersonAddress:
    """
    Represents an address assigned to a person.

    Attributes:
        id: The assignment ID.
        person_id: The ID of the person.
        address_id: The ID of the assigned address.
        address_type_id: The ID of the address type (e.g. permanent, mailing).
        validity: The period during which the address belongs to the person.
    """

    def __init__(
        self,
        id: int | None,
        person_id: int,
        address_id: int,
        address_type_id: int,
        validity: ValidityPeriod,
    ):
        self.id = id
        self.person_id = person_id
        self.address_id = address_id
        self.address_type_id = address_type_id
        self.validity = validity

    @classmethod
    def assign(
        cls,
        person: Person,
        address: Address,
        address_type: AddressType,
        current_time: datetime,
    ) -> Self:
        """
        Assign address to person, valid from now on

        Args:
            person: The person the address belongs to.
            address: The assigned address.
            address_type: The type of the address.
            current_time: The current time.

        Returns:
            The newly created assignment.
        """
        return cls(
            id=None,
            person_id=person.id,
            address_id=address.id,
            address_type_id=address_type.id,
            validity=ValidityPeriod(valid_from=current_time),
        )

    def end(self, current_time: datetime) -> None:
        """
        Ends the validity of the assignment, e.g. when the person moves.

        Args:
            current_time: The current time.

        Raises:
            PersonValidationError: If the assignment is not active at current_time.
        """
        self._validate_end(current_time)

        self.validity = ValidityPeriod(valid_from=self.validity.valid_from, valid_to=current_time)

    def is_active(self, current_time: datetime) -> bool:
        """
        Check if the assignment is active at the given time.

        Args:
            current_time: The time to check.

        Returns:
            True if the assignment is active, False otherwise.
        """
        return self.validity.is_active(current_time)

    def _validate_end(self, current_time: datetime) -> None:
        """
        Validates that the assignment can be ended.

        Raises:
            PersonValidationError: If the assignment is not active at current_time.
        """
        if not self.is_active(current_time):
            raise PersonValidationError("Only an active address assignment can be ended.")
