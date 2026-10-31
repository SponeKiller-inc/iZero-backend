from app.application.seed_data.legal_forms import LEGAL_FORMS
from app.domain.shared.entities.legal_form import LegalForm
from app.domain.shared.repositories.legal_form import LegalFormRepository


class SeedDefaultLegalForms:
    """Ensures the catalogue of legal forms is created"""

    def __init__(self, legal_form_repository: LegalFormRepository) -> None:
        self.legal_form_repository = legal_form_repository

    def execute(self) -> None:
        """
        Inserts missing legal forms and overwrites the name of existing ones.
        """
        for code, name in LEGAL_FORMS:
            legal_form = self.legal_form_repository.get_by_code(code)

            if legal_form is None:
                legal_form = LegalForm.create(code=code, name=name)
            else:
                legal_form.update(code=code, name=name)

            self.legal_form_repository.save(legal_form)
