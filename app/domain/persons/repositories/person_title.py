from datetime import datetime
from typing import Protocol

from app.domain.persons.entities.person_title import PersonTitle


class PersonTitleRepository(Protocol):
    def get(self, person_id: int, ref_date: datetime) -> list[PersonTitle]:
        """
        Get title assignments of the person valid at the reference date

        Args:
            person_id: Person ID
            ref_date: Reference date

        Returns:
            List of PersonTitle entities, empty if the person holds no title
        """
        ...

    def save(self, person_title: PersonTitle) -> PersonTitle:
        """
        Save new or existing title assignment

        Args:
            person_title: PersonTitle entity to save

        Returns:
            Saved person title entity
        """
        ...
