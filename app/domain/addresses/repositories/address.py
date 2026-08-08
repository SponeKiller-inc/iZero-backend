from typing import Protocol, Optional
from app.domain.addresses.entities.address import Address

class AddressRepository(Protocol):
    def get(self, address_id: int) -> Optional[Address]:
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
        
    def save(self, address: Address) -> Address:
        """
        Save new or existing address
        
        Args:
            address: Address entity to save
            
        Returns:
            Saved address entity
        """
        ...
