from typing import Self

from app.domain.shared.entities.phone_prefix import PhonePrefix
from app.domain.shared.value_objects.contact import PhoneNumber


class Phone:
    """
    Represents a phone number together with its calling code.

    Attributes:
        id: The phone ID.
        phone_prefix_id: The ID of the calling code from the phone prefix catalogue.
        number: The national phone number.
    """

    def __init__(
        self,
        id: int | None,
        phone_prefix_id: int,
        number: PhoneNumber,
    ):
        self.id = id
        self.phone_prefix_id = phone_prefix_id
        self.number = number

    @classmethod
    def create(cls, prefix: PhonePrefix, number: PhoneNumber) -> Self:
        """
        Creates a new phone.

        Args:
            prefix: The calling code from the phone prefix catalogue.
            number: The national phone number.

        Returns:
            The newly created phone.
        """
        return cls(id=None, phone_prefix_id=prefix.id, number=number)
