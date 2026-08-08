from typing import Optional, Self

class Role:
    """
    Represents the role entity.

    Attributes:
        id: The role ID.
        name: The name of the role.
        disabled: Indicates whether the role is disabled.
    """
    def __init__(self, name: str, id: Optional[int] = None, disabled: bool = False):
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
        """
        return cls(id=0, name=name)

    def delete(self) -> None:
        """
        Deletes the role (soft delete).
        
        Raises:
            ValueError: If attempting to delete the 'regular' role.
        """
        if self.name.lower() == "regular":
            raise ValueError("Role 'regular' cannot be deleted.")
        self.disabled = True
