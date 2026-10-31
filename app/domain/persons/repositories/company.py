from typing import Protocol

from app.domain.persons.entities.company import Company


class CompanyRepository(Protocol):
    def get_by_person_id(self, person_id: int) -> Company | None:
        """
        Get company details by person ID

        Args:
            person_id: Person ID

        Returns:
            Company entity if found, else None
        """
        ...

    def get_by_registration_number(self, registration_number: str) -> Company | None:
        """
        Get company details by company registration number

        Args:
            registration_number: Company registration number

        Returns:
            Company entity if found, else None
        """
        ...

    def save(self, company: Company) -> Company:
        """
        Save new or existing company details

        Args:
            company: Company entity to save

        Returns:
            Saved company entity
        """
        ...
