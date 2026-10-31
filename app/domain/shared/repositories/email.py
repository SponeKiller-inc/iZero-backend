from typing import Protocol

from app.domain.shared.entities.email import Email


class EmailRepository(Protocol):
    def get(self, email_id: int) -> Email | None:
        """
        Get e-mail by ID

        Args:
            email_id: E-mail ID

        Returns:
            Email entity if found, else None
        """
        ...

    def get_by_address(self, address: str) -> Email | None:
        """
        Get e-mail by its address

        Args:
            address: E-mail address

        Returns:
            Email entity if found, else None
        """
        ...

    def save(self, email: Email) -> Email:
        """
        Save new e-mail; a stored e-mail is shared by every record using it and cannot
        be changed, so an existing one is returned unchanged

        Args:
            email: Email entity to save

        Returns:
            Saved e-mail entity
        """
        ...
