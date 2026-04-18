from abc import ABC, abstractmethod

from app.models.user_roles import UserRoles

class ICustomerRepository(ABC):
    @abstractmethod
    def get(self, user_id: int, customer_id: int) -> list['Customers'] | None: # type: ignore
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> str | None:
        pass

    @abstractmethod
    def add(self, new_customer: 'Customers') -> 'Customers': # type: ignore
        pass

    @abstractmethod
    def update(self, user_id: int, role_type_id: int) -> UserRoles:
        pass
