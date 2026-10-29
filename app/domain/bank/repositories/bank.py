from typing import Protocol

from app.domain.bank.entities.bank import Bank


class BankRepository(Protocol):
    def get(self, bank_id: int) -> Bank | None:
        """
        Get bank by ID

        Args:
            bank_id: Bank ID

        Returns:
            Bank entity if found, else None
        """
        ...

    def get_by_code(self, code: str) -> Bank | None:
        """
        Get bank by its national bank code

        Args:
            code: National bank code

        Returns:
            Bank entity if found, else None
        """
        ...

    def get_all(self) -> list[Bank]:
        """
        Get all banks of the catalogue

        Returns:
            List of Bank entities
        """
        ...

    def save(self, bank: Bank) -> Bank:
        """
        Save new or existing bank

        Args:
            bank: Bank entity to save

        Returns:
            Saved bank entity
        """
        ...
