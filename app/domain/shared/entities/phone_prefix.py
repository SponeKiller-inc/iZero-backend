from typing import Self


class PhonePrefix:
    """
    Represents an international calling code from the phone prefix catalogue (e.g. "420").

    Attributes:
        id: The phone prefix ID.
        prefix: The calling code as digits only, without the leading "+" or "00".
        country_id: The ID of the country the calling code belongs to.
    """

    MAX_LENGTH = 3

    def __init__(
        self,
        id: int | None,
        prefix: str,
        country_id: int,
    ):
        self.id = id
        self.prefix = prefix
        self.country_id = country_id

    @classmethod
    def create(cls, prefix: str, country_id: int) -> Self:
        """
        Creates a new phone prefix.

        Args:
            prefix: The calling code as digits only, without the leading "+" or "00".
            country_id: The ID of the country the calling code belongs to.

        Returns:
            The newly created phone prefix.

        Raises:
            ValueError: If prefix is not 1–3 digits.
        """
        cls._validate(prefix)

        return cls(id=None, prefix=prefix, country_id=country_id)

    def update(self, prefix: str, country_id: int) -> None:
        """
        Updates the phone prefix.

        Args:
            prefix: The calling code as digits only, without the leading "+" or "00".
            country_id: The ID of the country the calling code belongs to.

        Raises:
            ValueError: If prefix is not 1–3 digits.
        """
        self._validate(prefix)

        self.prefix = prefix
        self.country_id = country_id

    @classmethod
    def _validate(cls, prefix: str) -> None:
        """
        Validates the fields shared by `create` and `update`.

        Raises:
            ValueError: If prefix is not 1–3 digits.
        """
        if not prefix or not prefix.isdigit() or len(prefix) > cls.MAX_LENGTH:
            raise ValueError(f"Phone prefix must be 1–{cls.MAX_LENGTH} digits without '+' or '00', got '{prefix}'.")
