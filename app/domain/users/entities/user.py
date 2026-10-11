from __future__ import annotations

from typing import Self

from app.domain.users.constants.admin import ADMIN_EMAIL
from app.domain.users.constants.registration_source_type import RegistrationSourceType
from app.domain.users.exceptions.user import UserInactiveError, UserProtectedError
from app.domain.users.value_objects.registration_source import RegistrationSource


class User:
    """
    Represents a user.
    
    Attributes:
        id: The user ID.
        email: The user email.
        password: The user password.
        provider_user_id: The provider user ID.
        provider: The provider.
        is_active: False once the user has been soft deleted.
    """
    
    def __init__(
        self,   
        id: int | None, 
        email: str,
        provider: RegistrationSource,
        password: str | None = None, 
        provider_user_id: str | None = None,
        is_active: bool = True,
    ):
        self.id = id
        self.email = email.lower()
        self.password = password
        self.provider_user_id = provider_user_id
        self.provider = provider
        self.is_active = is_active

    @classmethod
    def create_local(
        cls,
        email: str,
        password: str
    ) -> Self:
        """
        Creates a new user locally.
        """
        return cls(
            id=None,
            email=email,
            provider=RegistrationSource(RegistrationSourceType.LOCAL),
            password=password,
        )
    
    @classmethod
    def create_admin(
        cls,
        password: str
    ) -> Self:
        """
        Creates the bootstrap admin user locally. Reserved for SeedDefaultAdmin.
        """
        return cls(
            id=None,
            email=ADMIN_EMAIL,
            provider=RegistrationSource(RegistrationSourceType.SEED),
            password=password,
        )

    @classmethod
    def create_oauth(
        cls,
        email: str,
        provider_user_id: str
    ) -> Self:
        """
        Creates a new user via oauth provider.
        """
        return cls(
            id=None,
            email=email,
            provider=RegistrationSource(RegistrationSourceType.OAUTH),
            provider_user_id=provider_user_id,
        )

    def is_protected(self) -> bool:
        """
        Whether the user is the bootstrap admin, which must never be deleted.
        """
        return self.email == ADMIN_EMAIL

    def deactivate(self) -> None:
        """
        Soft deletes the user.

        Raises:
            UserInactiveError: If the user is already inactive.
            UserProtectedError: If the user is the bootstrap admin.
        """
        if not self.is_active:
            raise UserInactiveError("User is already inactive")

        if self.is_protected():
            raise UserProtectedError("Bootstrap admin cannot be deactivated")

        self.is_active = False
