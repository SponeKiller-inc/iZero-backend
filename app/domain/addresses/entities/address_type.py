from typing import Self


class AddressType:
    """
    Represents the address-type entity (e.g. permanent/mailing), referenced
    by user_addresses/bank_addresses/customer_addresses.

    Attributes:
        id: The address type ID.
        type: The type of the address ("permanent" or "mailing").
        description: The description of the address type.
    """

    def __init__(
        self,
        type: str,
        description: str,
        id: int | None = None,
    ):
        self.id = id
        self.type = type
        self.description = description

    @classmethod
    def create(cls, type: str, description: str) -> Self:
        """
        Creates a new address type.

        Args:
            type: The type of the address ("permanent" or "mailing").
            description: The description of the address type.

        Returns:
            The newly created address type.

        Raises:
            ValueError: If type is empty/blank or not lowercase.
        """
        if not type or not type.strip():
            raise ValueError("Address type's type must be a non-empty string.")
        if type != type.lower():
            raise ValueError(
                f"Address type's type must be lowercase, got '{type}'."
            )

        return cls(type=type, description=description)
