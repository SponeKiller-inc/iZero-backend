from typing import Self

from app.domain.shared.constants.title_type import TITLE_PREFIX_NAME, TITLE_SUFFIX_NAME


class Title:
    """
    Represents an academic title from the title catalogue (e.g. "Ing." or "Ph.D.").

    Attributes:
        id: The title ID.
        title_type: Whether the title is written before ("prefix") or after ("suffix") the name.
        name: The abbreviation of the title as written next to the name.
        priority: Order of the title among titles of the same type; the lower, the closer
            to the beginning of the full name.
    """

    ALLOWED_TYPES = (TITLE_PREFIX_NAME, TITLE_SUFFIX_NAME)

    def __init__(
        self,
        id: int | None,
        title_type: str,
        name: str,
        priority: int,
    ):
        self.id = id
        self.title_type = title_type
        self.name = name
        self.priority = priority

    @classmethod
    def create(
        cls,
        title_type: str,
        name: str,
        priority: int,
    ) -> Self:
        """
        Creates a new title.

        Args:
            title_type: "prefix" or "suffix".
            name: The abbreviation of the title.
            priority: Order of the title among titles of the same type.

        Returns:
            The newly created title.

        Raises:
            ValueError: If title_type is not allowed or name is empty/blank.
        """
        cls._validate(title_type, name)

        return cls(
            id=None,
            title_type=title_type,
            name=name,
            priority=priority,
        )

    def update(self, title_type: str, name: str, priority: int) -> None:
        """
        Updates the title.

        Args:
            title_type: "prefix" or "suffix".
            name: The abbreviation of the title.
            priority: Order of the title among titles of the same type.

        Raises:
            ValueError: If title_type is not allowed or name is empty/blank.
        """
        self._validate(title_type, name)

        self.title_type = title_type
        self.name = name
        self.priority = priority

    @classmethod
    def _validate(cls, title_type: str, name: str) -> None:
        """
        Validates the fields shared by `create` and `update`.

        Raises:
            ValueError: If title_type is not allowed or name is empty/blank.
        """
        if title_type not in cls.ALLOWED_TYPES:
            raise ValueError(f"title_type must be one of {cls.ALLOWED_TYPES}, got '{title_type}'.")
        if not name or not name.strip():
            raise ValueError("Title's name must be a non-empty string.")
