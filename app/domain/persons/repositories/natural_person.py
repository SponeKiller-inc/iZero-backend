from typing import Protocol

from app.domain.persons.entities.natural_person import NaturalPerson


class NaturalPersonRepository(Protocol):
    def get_by_person_id(self, person_id: int) -> NaturalPerson | None:
        """
        Get natural person details by person ID

        Args:
            person_id: Person ID

        Returns:
            NaturalPerson entity if found, else None
        """
        ...

    def save(self, natural_person: NaturalPerson) -> NaturalPerson:
        """
        Save new or existing natural person details together with their titles

        Args:
            natural_person: NaturalPerson entity to save

        Returns:
            Saved natural person entity
        """
        ...
