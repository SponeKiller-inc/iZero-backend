from __future__ import annotations
from typing import List, Optional, Self
from datetime import datetime
import uuid

from app.domain.shared.value_objects.period import ValidityPeriod
from app.application.ports.time_provider import TimeProvider
from app.domain.session.value_objects.session_event import SessionEvent
from app.domain.session.exceptions.session import SessionExpiredError


class Session:
    def __init__(
        self,
        id: Optional[int],
        external_id: uuid.UUID,
        validity: ValidityPeriod,
        ip_address: str,
        user_agent: str,
        user_id: Optional[int] = None,
        events: Optional[List[SessionEvent]] = None
    ) -> None:
        """
        Initializes a new session.

        Args:
            session_id (int | None): The unique identifier of the session.
             Optional for new sessions.
            external_id (uuid.UUID): The external identifier of the session.
            validity (ValidityPeriod): The validity period of the session.
            ip_address (str): The IP address from which the session was initiated.
            user_agent (str): The user agent string.
            user_id (int | None): The User id associated with the session. 
                Optional for non-logged in users
            events (List[SessionEvent] | None): The list of events associated with the session.
        """
        self.id = id
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
    ) -> Self:
        """
        Create new session

        Args:
            user_id (int | None): The User ID associated with the session.
            ip_address (str): The IP address from which the session was initiated.
            user_agent (str): The user agent string.
            expire_at (datetime): The expiration time of the session.
            current_time (datetime): The current time.

        Returns:
            Session: New session

        Raises:
            ValueError: If valid_from is after valid_to.
            
        """
        validity = ValidityPeriod(valid_from=current_time, valid_to=expire_at)
        session = cls(
            id=None,
            external_id=uuid.uuid4(),
            validity=validity,
            ip_address=ip_address,
            user_agent=user_agent,
            user_id=user_id
        )
        session.record_event("session_initialized", current_time)
        return session

    def record_event(self, event_type: str, current_time: datetime) -> None:
        """
        Records session event
        
        Args:
            event_type (str): The type of event.
            current_time (datetime): The current time.
            
        Raises:
            SessionExpiredError: If session is expired
        """
        if not self.validity.is_active(current_time):
            raise SessionExpiredError('Cannot add new event on expired session')
            
        new_event = SessionEvent(event_type, current_time)
        self.events.append(new_event)

    def is_expired(self, ref_time: datetime) -> bool:
        """
        Check if session is expired
        
        Args:
            ref_time (datetime): The reference time.
            
        Returns:
            bool: True if session is expired, False otherwise
        """
        return not self.validity.is_active(ref_time)

    def expire_now(self, time_provider: TimeProvider) -> None:
        """
        Expires the session immediately
        
        Args:
            time_provider (TimeProvider): The time provider.
        """
        now = time_provider.now()
        self.validity = ValidityPeriod(
            valid_from=self.validity.valid_from, 
            valid_to=now
        )
        self.record_event("user_logged_out", now)