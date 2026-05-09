from typing import List, Optional
from datetime import datetime
import uuid

from app.domain.shared.value_objects.period import ValidityPeriod
from app.domain.session.constants.session_event import SessionEvent

class Session:
    def __init__(
        self,
        session_id: Optional[int],
        external_id: uuid.UUID,
        validity: ValidityPeriod,
        ip_address: str,
        user_agent: str,
        user_id: Optional[int] = None,
        events: Optional[List[SessionEvent]] = None
    ):
        self.id = session_id
        self.external_id = external_id
        self.validity = validity
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.user_id = user_id
        self.events = events or []

    @classmethod
    def create_new(
        cls, 
        user_id: Optional[int], 
        ip_address: str, 
        user_agent: str, 
        expire_at: datetime,
        current_time: datetime
    ) -> "Session":
        """Factory metoda pro novou session."""
        validity = ValidityPeriod(valid_from=current_time, valid_to=expire_at)
        session = cls(
            session_id=None,
            external_id=uuid.uuid4(),
            validity=validity,
            ip_address=ip_address,
            user_agent=user_agent,
            user_id=user_id
        )
        session.record_event("session_initialized", current_time)
        return session

    def record_event(self, event_type: str, current_time: datetime) -> None:
        """Přidá událost do historie session."""
        if not self.validity.is_active(current_time):
            # Zde může být doménová výjimka, pokud je session po smrti
            pass
            
        new_event = SessionEvent(event_type, current_time)
        self.events.append(new_event)

    def is_expired(self, current_time: datetime) -> bool:
        return not self.validity.is_active(current_time)

    def expire_now(self, current_time: datetime) -> None:
        """Okamžité ukončení platnosti (např. při logoutu)."""
        self.validity = ValidityPeriod(
            valid_from=self.validity.valid_from, 
            valid_to=current_time
        )
        self.record_event("user_logged_out", current_time)