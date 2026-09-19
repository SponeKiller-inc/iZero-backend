from app.domain.shared.constants.title_type import (
    TITLE_PREFIX_ID,
    TITLE_PREFIX_NAME,
    TITLE_SUFFIX_ID,
    TITLE_SUFFIX_NAME,
)
from app.domain.shared.entities.title import Title
from app.domain.shared.repositories.title import TitleRepository


class SeedDefaultTitles:
    """Ensures the fixed prefix/suffix title-type rows exist under their fixed IDs."""

    def __init__(self, title_repository: TitleRepository) -> None:
        self.title_repository = title_repository

    def execute(self) -> None:
        for title_id, title_type in (
            (TITLE_PREFIX_ID, TITLE_PREFIX_NAME),
            (TITLE_SUFFIX_ID, TITLE_SUFFIX_NAME),
        ):
            if self.title_repository.get(title_id) is None:
                self.title_repository.save(Title(id=title_id, title_type=title_type))
