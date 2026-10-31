from app.domain.shared.entities.legal_form import LegalForm
from app.infrastructure.models.lookup.legal_forms import LegalFormModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyLegalFormRepository(BaseAlchemyRepository):
    def get(self, legal_form_id: int) -> LegalForm | None:
        """
        Get legal form by ID

        Args:
            legal_form_id: Legal form ID

        Returns:
            LegalForm entity if found, else None
        """

        model = (
            self.db
                .query(LegalFormModel)
                .filter(LegalFormModel.id == legal_form_id)
                .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_code(self, code: str) -> LegalForm | None:
        """
        Get legal form by its code

        Args:
            code: Abbreviation of the legal form

        Returns:
            LegalForm entity if found, else None
        """

        model = (
            self.db
                .query(LegalFormModel)
                .filter(LegalFormModel.code == code)
                .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def save(self, legal_form: LegalForm) -> LegalForm:
        """
        Save new or existing legal form

        Args:
            legal_form: LegalForm entity to save

        Returns:
            Saved legal form entity
        """

        if legal_form.id is None:
            return self._insert(legal_form)
        else:
            return self._update(legal_form)

    def _insert(self, legal_form: LegalForm) -> LegalForm:
        model = LegalFormModel(code=legal_form.code, name=legal_form.name)
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, legal_form: LegalForm) -> LegalForm:
        model = (
            self.db
                .query(LegalFormModel)
                .filter(LegalFormModel.id == legal_form.id)
                .first()
        )

        model.code = legal_form.code
        model.name = legal_form.name

        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: LegalFormModel) -> LegalForm:
        return LegalForm(id=model.id, code=model.code, name=model.name)
