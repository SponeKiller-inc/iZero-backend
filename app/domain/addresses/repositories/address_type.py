from typing import Protocol

from app.domain.addresses.entities.address_type import AddressType


class AddressTypeRepository(Protocol):
    """Repository interface for AddressType entity."""

    def get_by_type(self, address_type: str) -> AddressType | None:
        """
        Get an address type by its natural-key type ("permanent" or "mailing").

        Args:
            address_type: The type of the address type row.

        Returns:
            The AddressType entity if found, None otherwise.
        """
        ...

    def save(self, address_type: AddressType) -> AddressType:
        """
        Create a new address type.

        Args:
            address_type: The address type to create.

        Returns:
            The created AddressType entity.
        """
        ...
