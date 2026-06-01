from typing import Protocol

from app.domain.session.entities.session import Session

class SessionRepository(Protocol):
    def get_last_user_session(self, user_id: int) -> Session | None:
        ...

    def get_by_external_id(self, external_id: str) -> Session | None:
        ...

    def insert(self, new_session: Session) -> Session:
        ...

    def update(self, updated_session: Session) -> Session:
        ...
    