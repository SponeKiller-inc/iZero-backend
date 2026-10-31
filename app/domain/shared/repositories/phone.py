from typing import Protocol

from app.domain.shared.entities.phone import Phone


class PhoneRepository(Protocol):
    def get(self, phone_id: int) -> Phone | None:
        """
        Get phone by ID

        Args:
            phone_id: Phone ID

        Returns:
            Phone entity if found, else None
        """
        ...

    def get_by_number(self, phone_prefix_id: int, number: str) -> Phone | None:
        """
        Get phone by its calling code and national number

        Args:
            phone_prefix_id: Phone prefix ID
            number: National phone number

        Returns:
            Phone entity if found, else None
        """
        ...

    def save(self, phone: Phone) -> Phone:
        """
        Save new phone; a stored phone is shared by every record using it and cannot
        be changed, so an existing one is returned unchanged

        Args:
            phone: Phone entity to save

        Returns:
            Saved phone entity
        """
        ...
