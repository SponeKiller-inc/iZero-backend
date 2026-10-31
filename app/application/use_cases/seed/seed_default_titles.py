from app.application.seed_data.titles import PREFIX_TITLES, SUFFIX_TITLES
from app.domain.shared.constants.title_type import TITLE_PREFIX_NAME, TITLE_SUFFIX_NAME
from app.domain.shared.entities.title import Title
from app.domain.shared.repositories.title import TitleRepository


class SeedDefaultTitles:
    """Ensures the catalogue of academic titles is created"""

    def __init__(self, title_repository: TitleRepository) -> None:
        self.title_repository = title_repository

    def execute(self) -> None:
        """
        Inserts missing titles and overwrites the priority of existing ones.
        """
        for title_type, titles in (
            (TITLE_PREFIX_NAME, PREFIX_TITLES),
            (TITLE_SUFFIX_NAME, SUFFIX_TITLES),
        ):
            for name, priority in titles:
                title = self.title_repository.get_by_name(title_type, name)

                if title is None:
                    title = Title.create(
                        title_type=title_type,
                        name=name,
                        priority=priority,
                    )
                else:
                    title.update(title_type=title_type, name=name, priority=priority)

                self.title_repository.save(title)
