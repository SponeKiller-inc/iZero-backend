from typing import Self

from app.domain.shared.value_objects.location import CountryIsoCode


class Country:
    """
    Represents a country.

    Attributes:
        id: The country ID.
        code: The ISO 3166-1 alpha-3 country code.
        name: The country name.
    """

    def __init__(
        self,
        id: int | None,
        code: CountryIsoCode,
        name: str,
    ):
        self.id = id
        self.code = code
        self.name = name

    @classmethod
    def create(cls, code: CountryIsoCode, name: str) -> Self:
        """
        Creates a new country.

        Args:
            code: The ISO 3166-1 alpha-3 country code.
            name: The country name.

        Returns:
            The newly created country.

        Raises:
            ValueError: If name is empty or blank.
        """
        if not name.strip():
            raise ValueError("Country name must be a non-empty string.")
        return cls(id=None, code=code, name=name)
