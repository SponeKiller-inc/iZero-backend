from dataclasses import dataclass


@dataclass
class InitializeSessionIn:
    """
    Input DTO for InitializeSession use-case
    """
    user_id: int | None
    ip_address: str
    user_agent: str
    external_id: str | None

@dataclass
class InitializeSessionOut:
    """
    Output DTO for InitializeSession use-case
    """
    id: int
    external_id: str