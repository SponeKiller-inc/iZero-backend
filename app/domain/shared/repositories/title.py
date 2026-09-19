from typing import Protocol, Optional
from app.domain.shared.entities.title import Title

class TitleRepository(Protocol):
    """Repository interface for Title entity."""

    def get(self, title_id: int) -> Optional[Title]:
        """
        Get a title by its ID.

        Args:
            title_id: The ID of the title.

        Returns:
            The Title entity if found, None otherwise.
        """
        ...

    def save(self, title: Title) -> Title:
        """
        Create a new title. If title.id is set, it is persisted as-is (used for seeding fixed IDs).

        Args:
            title: The title to create.

        Returns:
            The created Title entity.
        """
        ...
