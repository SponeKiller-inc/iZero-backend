from typing import Self


class AddressType:
    """
    Represents the address-type entity (e.g. permanent/mailing), referenced by user_addresses/bank_addresses/customer_addresses.

    Attributes:
        id: The address type ID.
        description: The description of the address type.
    """

    def __init__(
        self,
        id: int | None,
        description: str,
    ):
        self.id = id
        self.description = description

    @classmethod
    def create(cls, description: str) -> Self:
        """
        Creates a new address type.

        Args:
            description: The description of the address type.

        Returns:
            The newly created address type.

        Raises:
            ValueError: If description is empty or blank.
        """
        if not description.strip():
            raise ValueError("Address type description must be a non-empty string.")
        return cls(id=None, description=description)
