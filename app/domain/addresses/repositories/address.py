from typing import Protocol

from app.domain.addresses.entities.address import Address


class AddressRepository(Protocol):
    def get(self, address_id: int) -> Address | None:
        """
        Get address by ID
        
        Args:
            address_id: Address ID
            
        Returns:
            Address entity if found, else None
        """
        ...

    def get_all(self) -> list[Address]:
        """
        Get all addresses
        
        Returns:
            List of Address entities
        """
        ...

    def get_by_external_id(self, external_id: int, country_id: int) -> Address | None:
        """
        Get address by its external (e.g. RÚIAN) ID and country

        Args:
            external_id: External address ID
            country_id: ID of the country the address belongs to

        Returns:
            Address entity if found, else None
        """
        ...

    def exists_for_country(self, country_id: int) -> bool:
        """
        Check whether any address already exists for the given country

        Args:
            country_id: Country ID

        Returns:
            True if at least one address exists for the country, else False
        """
        ...

    def upsert_many(self, addresses: list[Address]) -> None:
        """
        Bulk insert addresses, overwriting existing ones matched by external
        ID and country. Existing addresses keep their ID.

        Args:
            addresses: Address entities to insert or update; their `id` is
                ignored. If the same external ID and country appear more
                than once, the last occurrence wins.
        """
        ...

    def save(self, address: Address) -> Address:
        """
        Save new or existing address
        
        Args:
            address: Address entity to save
            
        Returns:
            Saved address entity
        """
        ...
