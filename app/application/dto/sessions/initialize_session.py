from dataclasses import dataclass
from typing import Optional

@dataclass
class InitializeSessionIn:
    """
    Input DTO for InitializeSession use-case
    """
    user_id: Optional[int]
    ip_address: str
    user_agent: str
    external_id: Optional[str]

@dataclass
class InitializeSessionOut:
    """
    Output DTO for InitializeSession use-case
    """
    external_id: str