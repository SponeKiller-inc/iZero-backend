from typing import Self


class LegalForm:
    """
    Represents a legal form of a company from the legal form catalogue (e.g. "s.r.o.").

    Attributes:
        id: The legal form ID.
        code: The abbreviation of the legal form as written after the company name.
        name: The full name of the legal form.
    """

    def __init__(
        self,
        id: int | None,
        code: str,
        name: str,
    ):
        self.id = id
        self.code = code
        self.name = name

    @classmethod
    def create(cls, code: str, name: str) -> Self:
        """
        Creates a new legal form.

        Args:
            code: The abbreviation of the legal form.
            name: The full name of the legal form.

        Returns:
            The newly created legal form.

        Raises:
            ValueError: If code or name is empty/blank.
        """
        cls._validate(code, name)

        return cls(id=None, code=code, name=name)

    def update(self, code: str, name: str) -> None:
        """
        Updates the legal form.

        Args:
            code: The abbreviation of the legal form.
            name: The full name of the legal form.

        Raises:
            ValueError: If code or name is empty/blank.
        """
        self._validate(code, name)

        self.code = code
        self.name = name

    @staticmethod
    def _validate(code: str, name: str) -> None:
        """
        Validates the fields shared by `create` and `update`.

        Raises:
            ValueError: If code or name is empty/blank.
        """
        if not code or not code.strip():
            raise ValueError("Legal form's code must be a non-empty string.")
        if not name or not name.strip():
            raise ValueError("Legal form's name must be a non-empty string.")
