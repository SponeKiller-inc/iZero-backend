from datetime import datetime
from typing import Self

from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions.person import PersonValidationError
from app.domain.shared.entities.title import Title
from app.domain.shared.value_objects.period import ValidityPeriod


class PersonTitle:
    """
    Represents an academic title assigned to a person.

    Attributes:
        id: The assignment ID.
        person_id: The ID of the person.
        title_id: The ID of the assigned title.
        validity: The period during which the person holds the title.
    """

    def __init__(
        self,
        id: int | None,
        person_id: int,
        title_id: int,
        validity: ValidityPeriod,
    ):
        self.id = id
        self.person_id = person_id
        self.title_id = title_id
        self.validity = validity

    @classmethod
    def assign(cls, person: Person, title: Title, current_time: datetime) -> Self:
        """
        Assign title to person, valid from now on

        Args:
            person: The person holding the title.
            title: The assigned title.
            current_time: The current time.

        Returns:
            The newly created assignment.

        Raises:
            PersonValidationError: If the person is not a natural person.
        """
        cls._validate(person)

        return cls(
            id=None,
            person_id=person.id,
            title_id=title.id,
            validity=ValidityPeriod(valid_from=current_time),
        )

    def end(self, current_time: datetime) -> None:
        """
        Ends the validity of the assignment, e.g. when the title is removed from the person.

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

    @staticmethod
    def _validate(person: Person) -> None:
        """
        Validates the assignment.

        Raises:
            PersonValidationError: If the person is not a natural person, as only
                natural persons hold academic titles.
        """
        if person.person_type != PersonType.NATURAL_PERSON:
            raise PersonValidationError("Only a natural person can hold an academic title.")

    def _validate_end(self, current_time: datetime) -> None:
        """
        Validates that the assignment can be ended.

        Raises:
            PersonValidationError: If the assignment is not active at current_time.
        """
        if not self.is_active(current_time):
            raise PersonValidationError("Only an active title assignment can be ended.")
