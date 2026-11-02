from typing import Protocol

from app.domain.users.entities.user_person import UserPerson


class UserPersonRepository(Protocol):
    def get_by_user_id(self, user_id: int) -> UserPerson | None:
        """
        Get person assignment of the user

        Args:
            user_id: User ID

        Returns:
            UserPerson entity if found, else None
        """
        ...

    def save(self, user_person: UserPerson) -> UserPerson:
        """
        Save new person assignment; a stored assignment cannot be changed, so an
        existing one is returned unchanged

        Args:
            user_person: UserPerson entity to save

        Returns:
            Saved user person entity
        """
        ...
