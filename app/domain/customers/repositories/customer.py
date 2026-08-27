from typing import Protocol
from app.domain.customers.entities.customer import Customer

class CustomerRepository(Protocol):
    def get(self, user_id: int, customer_id: int) -> Customer | None:
        """
        Get customer by user ID and customer ID
        
        Args:
            user_id: User ID
            customer_id: Customer ID
            
        Returns:
            Customer if found, else None
        """
        ...

    def get_all(self, user_id: int) -> list[Customer]:
        """
        Get all customers by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            List of customers, empty if none found
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
