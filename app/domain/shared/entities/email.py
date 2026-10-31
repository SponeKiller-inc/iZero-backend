from typing import Self

from app.domain.shared.value_objects.contact import EmailAddress


class Email:
    """
    Represents an e-mail address stored once and shared by every record using it.

    Attributes:
        id: The e-mail ID.
        address: The e-mail address.
    """

    def __init__(self, id: int | None, address: EmailAddress):
        self.id = id
        self.address = address

    @classmethod
    def create(cls, address: EmailAddress) -> Self:
        """
        Creates a new e-mail; the address is stored lowercase, as e-mail addresses
        are compared case-insensitively.

        Args:
            address: The e-mail address.

        Returns:
            The newly created e-mail.
        """
        return cls(id=None, address=EmailAddress(address.value.lower()))
