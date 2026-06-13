from typing import Protocol, Optional
from app.domain.users.entities.user import User

class UserRepository(Protocol):
    def get_user(self, user_id: str) -> Optional[User]:
        ...

    def get_user_local(self, email: str) -> Optional[User]:
        ...

    def get_user_google(self, provider_user_id: str) -> Optional[User]:
        ...

    def exists_local(self, email: str) -> bool:
        ...

    def exists_google(self, provider_user_id: str, email: str) -> bool:
        ...

    def exists_user(self, user_id: int) -> bool:
        ...

    def save(self, new_user: User) -> User:
        ...