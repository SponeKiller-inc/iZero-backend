from app.application.constants.use_case import UseCase
from app.application.dto.title.title import TitleOut
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.title import TitleRepository


class RetrieveTitles:

    def __init__(self, title_repository: TitleRepository) -> None:
        """
        Initialize use-case

        Args:
            title_repository: Title repository
        """
        self.title_repository = title_repository

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE_TITLES)
    def execute(self) -> list[TitleOut]:
        """
        Retrieve all titles of the catalogue

        Returns:
            List of all titles, empty if the catalogue is empty
        """
        return [
            TitleOut(
                id=title.id,
                title_type=title.title_type,
                name=title.name,
            )
            for title in self.title_repository.get_all()
        ]
