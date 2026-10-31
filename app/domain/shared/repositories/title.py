from typing import Protocol

from app.domain.shared.entities.title import Title


class TitleRepository(Protocol):
    """Repository interface for Title entity."""

    def get(self, title_ids: list[int]) -> list[Title]:
        """
        Get titles by their IDs

        Args:
            title_ids: Title IDs

        Returns:
            List of found Title entities, prefix titles first, each type ordered
            by priority; IDs that do not exist are left out
        """
        ...

    def get_by_name(self, title_type: str, name: str) -> Title | None:
        """
        Get title of the given type by its name

        Args:
            title_type: "prefix" or "suffix"
            name: Abbreviation of the title

        Returns:
            Title entity if found, else None
        """
        ...

    def save(self, title: Title) -> Title:
        """
        Save new or existing title

        Args:
            title: Title entity to save

        Returns:
            Saved Title entity
        """
        ...
