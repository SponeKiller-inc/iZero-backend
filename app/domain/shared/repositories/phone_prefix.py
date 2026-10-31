from typing import Protocol

from app.domain.shared.entities.phone_prefix import PhonePrefix


class PhonePrefixRepository(Protocol):
    def get(self, phone_prefix_id: int) -> PhonePrefix | None:
        """
        Get phone prefix by ID

        Args:
            phone_prefix_id: Phone prefix ID

        Returns:
            PhonePrefix entity if found, else None
        """
        ...

    def get_by_prefix(self, prefix: str) -> PhonePrefix | None:
        """
        Get phone prefix by its calling code

        Args:
            prefix: Calling code as digits only, without the leading "+" or "00"

        Returns:
            PhonePrefix entity if found, else None
        """
        ...

    def save(self, phone_prefix: PhonePrefix) -> PhonePrefix:
        """
        Save new or existing phone prefix

        Args:
            phone_prefix: PhonePrefix entity to save

        Returns:
            Saved phone prefix entity
        """
        ...
