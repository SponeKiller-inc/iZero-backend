from typing import Protocol, Optional
from app.domain.users.entities.user import User

class UserRepository(Protocol):
    def get(self, user_id: str) -> Optional[User]:
        ...

    def get_local(self, email: str) -> Optional[User]:
        ...

    def get_oauth_user(self, provider_user_id: str) -> Optional[User]:
        ...

    def exists_local(self, email: str) -> bool:
        ...

    def exists_oauth_user(self, provider_user_id: str) -> bool:
        ...

    def save(self, user: User) -> User:
        ...