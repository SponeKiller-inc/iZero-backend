from typing import Protocol, Optional
from app.domain.customers.entities.customer import Customer

class CustomerRepository(Protocol):
    def get(self, user_id: int, customer_id: int) -> Optional[list[Customer]]:
        """
        Get customer by user ID and customer ID
        
        Args:
            user_id: User ID
            customer_id: Customer ID
            
        Returns:
            Customer if found, else None
        """
        ...

    def get_all(self, user_id: int) -> Optional[str]:
        """
        Get all customers by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            Customer data if found
        """
        ...

    def save(self, customer: Customer) -> Customer:
        """
        Save new or existing customer
        
        Args:
            customer: Customer entity to save
            
        Returns:
            Saved customer entity
        """
        ...
