from app.application.constants.use_case import UseCase
from app.application.dto.legal_form.legal_form import LegalFormOut
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.legal_form import LegalFormRepository


class RetrieveLegalForms:

    def __init__(self, legal_form_repository: LegalFormRepository) -> None:
        """
        Initialize use-case

        Args:
            legal_form_repository: Legal form repository
        """
        self.legal_form_repository = legal_form_repository

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE_LEGAL_FORMS)
    def execute(self) -> list[LegalFormOut]:
        """
        Retrieve all legal forms of the catalogue

        Returns:
            List of all legal forms, empty if the catalogue is empty
        """
        return [
            LegalFormOut(
                id=legal_form.id,
                code=legal_form.code,
                name=legal_form.name,
            )
            for legal_form in self.legal_form_repository.get_all()
        ]
