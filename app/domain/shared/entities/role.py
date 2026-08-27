from typing import Self

from app.domain.shared.constants.role_type import REGULAR_ROLE_ID


class Role:
    """
    Represents the role entity.

    Attributes:
        id: The role ID.
        name: The name of the role.
        disabled: Indicates whether the role is disabled.
    """
    def __init__(
        self,
        name: str,
        id: int | None = None,
        disabled: bool = False,
    ):
        self.id = id
        self.name = name
        self.disabled = disabled

    @classmethod
    def create(cls, name: str) -> Self:
        """
        Creates a new role.

        Args:
            name: The name of the role.

        Returns:
            The newly created role.

        Raises:
            ValueError: If name is empty or blank.
        """
        if not name.strip():
            raise ValueError("Role name must be a non-empty string.")
        return cls(id=None, name=name)

    def delete(self) -> None:
        """
        Deletes the role (soft delete).

        Raises:
            ValueError: If attempting to delete the 'regular' role.
        """
        if self.id == REGULAR_ROLE_ID:
            raise ValueError("Role 'regular' cannot be deleted.")
        self.disabled = True
