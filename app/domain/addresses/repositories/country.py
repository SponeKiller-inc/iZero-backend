from typing import Protocol

from app.domain.addresses.entities.country import Country


class CountryRepository(Protocol):
    """Repository interface for Country entity."""

    def get(self, country_id: int) -> Country | None:
        """
        Get a country by its ID.

        Args:
            country_id: The ID of the country.

        Returns:
            The Country entity if found, None otherwise.
        """
        ...

    def get_by_code(self, code: str) -> Country | None:
        """
        Get a country by its ISO code.

        Args:
            code: The ISO 3166-1 alpha-3 country code.

        Returns:
            The Country entity if found, None otherwise.
        """
        ...

    def get_all(self) -> list[Country]:
        """
        Get all countries.

        Returns:
            List of Country entities.
        """
        ...

    def save(self, country: Country) -> Country:
        """
        Create a new country. If country.id is set, it is persisted as-is (used for seeding fixed IDs).

        Args:
            country: The country to create.

        Returns:
            The created Country entity.
        """
        ...
