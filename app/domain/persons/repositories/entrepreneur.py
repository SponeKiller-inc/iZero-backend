from typing import Protocol

from app.domain.persons.entities.entrepreneur import Entrepreneur


class EntrepreneurRepository(Protocol):
    def get_by_person_id(self, person_id: int) -> Entrepreneur | None:
        """
        Get entrepreneur details by person ID

        Args:
            person_id: Person ID

        Returns:
            Entrepreneur entity if found, else None
        """
        ...

    def get_by_registration_number(self, registration_number: str) -> Entrepreneur | None:
        """
        Get entrepreneur details by company registration number

        Args:
            registration_number: Company registration number

        Returns:
            Entrepreneur entity if found, else None
        """
        ...

    def save(self, entrepreneur: Entrepreneur) -> Entrepreneur:
        """
        Save new or existing entrepreneur details

        Args:
            entrepreneur: Entrepreneur entity to save

        Returns:
            Saved entrepreneur entity
        """
        ...
