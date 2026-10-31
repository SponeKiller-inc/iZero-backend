from typing import Protocol

from app.domain.persons.entities.person import Person


class PersonRepository(Protocol):
    def get(self, person_id: int) -> Person | None:
        """
        Get person by ID

        Args:
            person_id: Person ID

        Returns:
            Person entity if found, else None
        """
        ...

    def save(self, person: Person) -> Person:
        """
        Save new person; the person type cannot be changed, so an existing
        person is returned unchanged

        Args:
            person: Person entity to save

        Returns:
            Saved person entity
        """
        ...
