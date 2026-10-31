from datetime import datetime
from typing import Protocol

from app.domain.persons.entities.person_address import PersonAddress


class PersonAddressRepository(Protocol):
    def get(self, person_id: int, ref_date: datetime) -> list[PersonAddress]:
        """
        Get address assignments of the person valid at the reference date

        Args:
            person_id: Person ID
            ref_date: Reference date

        Returns:
            List of PersonAddress entities, empty if the person has no address
        """
        ...

    def save(self, person_address: PersonAddress) -> PersonAddress:
        """
        Save new or existing address assignment

        Args:
            person_address: PersonAddress entity to save

        Returns:
            Saved person address entity
        """
        ...
