from app.domain.shared.entities.title import Title
from app.domain.shared.repositories.title import TitleRepository
from app.infrastructure.models.lookup.titles import TitleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyTitleRepository(BaseAlchemyRepository, TitleRepository):
    def get_many(self, title_ids: list[int]) -> list[Title]:
        """
        Get titles by their IDs

        Args:
            title_ids (list[int]): title ids

        Returns:
            list[Title]: found titles, prefix titles first, each type ordered by priority;
            ids that do not exist are left out
        """

        if not title_ids:
            return []

        return [
            self._to_entity(model)
            for model in (
                self.db
                    .query(TitleModel)
                    .filter(TitleModel.id.in_(title_ids))
                    .order_by(TitleModel.title_type, TitleModel.priority, TitleModel.id)
                    .all()
            )
        ]

    def get_by_name(self, title_type: str, name: str) -> Title | None:
        """
        Get title of the given type by its name

        Args:
            title_type (str): "prefix" or "suffix"
            name (str): abbreviation of the title

        Returns:
            Title or None: title entity or None if no title found
        """

        model = (
            self.db
                .query(TitleModel)
                .filter(TitleModel.title_type == title_type, TitleModel.name == name)
                .first()
        )

        if model is None:
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

        if title.id is None:
            return self._insert(title)
        else:
            return self._update(title)

    def _insert(self, title: Title) -> Title:
        model = TitleModel(
            title_type=title.title_type,
            name=title.name,
            priority=title.priority,
        )
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, title: Title) -> Title:
        model = self.db.query(TitleModel).filter(TitleModel.id == title.id).first()

        model.title_type = title.title_type
        model.name = title.name
        model.priority = title.priority

        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: TitleModel) -> Title:
        return Title(
            id=model.id,
            title_type=model.title_type,
            name=model.name,
            priority=model.priority,
        )
