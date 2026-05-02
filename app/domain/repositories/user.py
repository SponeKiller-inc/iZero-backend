from abc import ABC, abstractmethod

from app.models.users import Users
from app.models.user_roles import UserRoles

class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> Users | None:
        pass

    @abstractmethod
    def get_user_local(self, email: str) -> Users | None:
        pass

    @abstractmethod
    def get_user_google(self, provider_user_id: str) -> Users | None:
        pass

    @abstractmethod
    def get_user_role(self, user_id: int) -> str | None:
        pass

    @abstractmethod
    def add_user_role(self, new_user_role: UserRoles) -> UserRoles:
        pass

    @abstractmethod
    def update_user_role(self, user_id: int, role_type_id: int) -> UserRoles:
        pass

    @abstractmethod
    def exists_local(self, email: str) -> bool:
        pass

    @abstractmethod
    def exists_google(self, provider_user_id: str, email: str) -> bool:
        pass

    @abstractmethod
    def exists_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def create_user(self, new_user: Users) -> Users:
        pass
