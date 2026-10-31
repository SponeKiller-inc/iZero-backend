from typing import Protocol

from app.domain.shared.entities.legal_form import LegalForm


class LegalFormRepository(Protocol):
    def get(self, legal_form_id: int) -> LegalForm | None:
        """
        Get legal form by ID

        Args:
            legal_form_id: Legal form ID

        Returns:
            LegalForm entity if found, else None
        """
        ...

    def get_by_code(self, code: str) -> LegalForm | None:
        """
        Get legal form by its code

        Args:
            code: Abbreviation of the legal form

        Returns:
            LegalForm entity if found, else None
        """
        ...

    def save(self, legal_form: LegalForm) -> LegalForm:
        """
        Save new or existing legal form

        Args:
            legal_form: LegalForm entity to save

        Returns:
            Saved legal form entity
        """
        ...
