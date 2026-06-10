from typing import Protocol

from app.domain.session.entities.session import Session

class SessionRepository(Protocol):
    def get(self, session_id: int) -> Session | None:
        ...

    def get_last_user_session(self, user_id: int) -> Session | None:
        ...

    def get_by_external_id(self, external_id: str) -> Session | None:
        ...

    def save(self, new_session: Session) -> Session:
        ...
