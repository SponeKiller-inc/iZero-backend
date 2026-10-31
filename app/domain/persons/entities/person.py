from typing import Self

from app.domain.persons.constants.person_type import PersonType


class Person:
    """
    Represents any party of iZero; holds only the person type, the details are kept
    in the type-specific record (natural person, entrepreneur or company).

    The person type is set once on creation and cannot be changed (BR-8).

    Attributes:
        id: The person ID.
        person_type: The type of the person.
    """

    def __init__(self, id: int | None, person_type: PersonType):
        self.id = id
        self.person_type = person_type

    @classmethod
    def create(cls, person_type: PersonType) -> Self:
        """
        Creates a new person.

        Args:
            person_type: The type of the person.

        Returns:
            The newly created person.
        """
        return cls(id=None, person_type=person_type)
