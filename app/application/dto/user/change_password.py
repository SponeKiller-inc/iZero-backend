from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChangePasswordIn:
    """
    Input DTO for ChangePassword use-case.
    """
    user_id: int
    current_password: str = field(repr=False)
    new_password: str = field(repr=False)
    password_confirmation: str = field(repr=False)
    session_id: int
