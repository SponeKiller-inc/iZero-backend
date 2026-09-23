
from app.domain.shared.entities.title import Title
from app.domain.shared.repositories.title import TitleRepository
from app.infrastructure.models.title.titles import TitleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyTitleRepository(BaseAlchemyRepository, TitleRepository):
    def get(self, title_id: int) -> Title | None:
        """
        Get a title by its ID

        Args:
            title_id (int): title id

        Returns:
            Title or None: title entity or None if no title found
        """

        model = self.db.query(TitleModel).filter(TitleModel.id == title_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, title: Title) -> Title:
        """
        Create or update Title.

        Args:
            title (Title): data to create or update title

        Returns:
            Title: newly created or updated title
        """
        # unlike other repos, title.id may be pre-assigned (seeding fixed IDs)
        # for a row that doesn't exist yet, so dispatch on actual row
        # existence rather than id nullness
        existing = (
            self.db.query(TitleModel).filter(TitleModel.id == title.id).first()
            if title.id is not None
            else None
        )

        if existing is None:
            return self._insert(title)
        return self._update(title, existing)

    def _insert(self, title: Title) -> Title:
        """
        Create Title. If title.id is set, it is persisted as-is (used for seeding fixed IDs).

        Args:
            title (Title): data to create title

        Returns:
            Title: newly created title
        """

        model = TitleModel(id=title.id, title_type=title.title_type)
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, title: Title, model: TitleModel) -> Title:
        """
        Update Title.

        Args:
            title (Title): data to update title
            model (TitleModel): existing title row

        Returns:
            Title: updated title
        """

        model.title_type = title.title_type
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: TitleModel) -> Title:
        return Title(id=model.id, title_type=model.title_type)

