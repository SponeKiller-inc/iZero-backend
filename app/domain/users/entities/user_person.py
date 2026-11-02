from typing import Self


class UserPerson:
    """
    Represents a person assigned to a user.

    Attributes:
        id: The assignment ID.
        user_id: The ID of the user the person belongs to.
        person_id: The ID of the assigned person.
    """

    def __init__(
        self,
        id: int | None,
        user_id: int,
        person_id: int,
    ):
        self.id = id
        self.user_id = user_id
        self.person_id = person_id

    @classmethod
    def assign(cls, user_id: int, person_id: int) -> Self:
        """
        Assign person to user

        Args:
            user_id: The ID of the user the person belongs to.
            person_id: The ID of the assigned person.

        Returns:
            The newly created assignment.
        """
        return cls(
            id=None,
            user_id=user_id,
            person_id=person_id,
        )
