from typing import Protocol

from app.models.sessions import Sessions
from app.models.session_log import SessionLog

class SessionRepository(Protocol):
    def get_last_user_session(self, user_id: int) -> Sessions | None:
        ...

    def get_session(self, external_id: str) -> Sessions | None:
        ...

    def create_session(self, new_session: Sessions) -> Sessions:
        ...

    def expire_session(self, session_id: int) -> None:
        ...

    def create_session_log(self, new_session_log: SessionLog) -> None:
        ...