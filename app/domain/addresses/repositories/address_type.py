from typing import Protocol

from app.domain.addresses.entities.address_type import AddressType


class AddressTypeRepository(Protocol):
    """Repository interface for AddressType entity."""

    def get(self, address_type_id: int) -> AddressType | None:
        """
        Get an address type by its ID.

        Args:
            address_type_id: The ID of the address type.

        Returns:
            The AddressType entity if found, None otherwise.
        """
        ...

    def save(self, address_type: AddressType) -> AddressType:
        """
        Create a new address type. If address_type.id is set, it is persisted as-is (used for seeding fixed IDs).

        Args:
            address_type: The address type to create.

        Returns:
            The created AddressType entity.
        """
        ...
