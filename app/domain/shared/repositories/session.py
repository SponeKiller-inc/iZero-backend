from abc import ABC, abstractmethod

from app.models.sessions import Sessions
from app.models.session_log import SessionLog

class ISessionRepository(ABC):
    @abstractmethod
    def get_last_user_session(self, user_id: int) -> Sessions | None:
        pass

    @abstractmethod
    def get_session(self, external_id: str) -> Sessions | None:
        pass

    @abstractmethod
    def create_session(self, new_session: Sessions) -> Sessions:
        pass

    @abstractmethod
    def expire_session(self, session_id: int) -> None:
        pass

    @abstractmethod
    def create_session_log(self, new_session_log: SessionLog) -> None:
        pass
