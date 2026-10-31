from app.domain.persons.entities.entrepreneur import Entrepreneur
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)
from app.infrastructure.models.person.entrepreneurs import EntrepreneurModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyEntrepreneurRepository(BaseAlchemyRepository):
    def get_by_person_id(self, person_id: int) -> Entrepreneur | None:
        """
        Get entrepreneur details by person ID

        Args:
            person_id: Person ID

        Returns:
            Entrepreneur entity if found, else None
        """

        entrepreneur_model = (
            self.db
                .query(EntrepreneurModel)
                .filter(EntrepreneurModel.person_id == person_id)
                .first()
        )

        if entrepreneur_model is None:
            return None

        return self._to_entity(entrepreneur_model)

    def get_by_registration_number(self, registration_number: str) -> Entrepreneur | None:
        """
        Get entrepreneur details by company registration number

        Args:
            registration_number: Company registration number

        Returns:
            Entrepreneur entity if found, else None
        """

        entrepreneur_model = (
            self.db
                .query(EntrepreneurModel)
                .filter(EntrepreneurModel.registration_number == registration_number)
                .first()
        )

        if entrepreneur_model is None:
            return None

        return self._to_entity(entrepreneur_model)

    def save(self, entrepreneur: Entrepreneur) -> Entrepreneur:
        """
        Save new or existing entrepreneur details

        Args:
            entrepreneur: Entrepreneur entity to save

        Returns:
            Saved entrepreneur entity
        """

        if entrepreneur.id is None:
            return self._insert(entrepreneur)
        else:
            return self._update(entrepreneur)

    def _insert(self, entrepreneur: Entrepreneur) -> Entrepreneur:
        entrepreneur_model = EntrepreneurModel(
            person_id=entrepreneur.person_id,
            name=entrepreneur.name,
            registration_number=entrepreneur.registration_number.value,
            vat_number=entrepreneur.vat_number.value if entrepreneur.vat_number else None,
            is_vat_payer=entrepreneur.is_vat_payer,
            phone_id=entrepreneur.phone_id,
            email_id=entrepreneur.email_id,
        )
        self.db.add(entrepreneur_model)
        self.db.flush()
        self.db.refresh(entrepreneur_model)

        return self._to_entity(entrepreneur_model)

    def _update(self, entrepreneur: Entrepreneur) -> Entrepreneur:
        entrepreneur_model = (
            self.db
                .query(EntrepreneurModel)
                .filter(EntrepreneurModel.id == entrepreneur.id)
                .first()
        )

        entrepreneur_model.name = entrepreneur.name
        entrepreneur_model.registration_number = entrepreneur.registration_number.value
        entrepreneur_model.vat_number = entrepreneur.vat_number.value if entrepreneur.vat_number else None
        entrepreneur_model.is_vat_payer = entrepreneur.is_vat_payer
        entrepreneur_model.phone_id = entrepreneur.phone_id
        entrepreneur_model.email_id = entrepreneur.email_id

        self.db.flush()
        self.db.refresh(entrepreneur_model)

        return self._to_entity(entrepreneur_model)

    def _to_entity(self, entrepreneur_model: EntrepreneurModel) -> Entrepreneur:
        return Entrepreneur(
            id=entrepreneur_model.id,
            person_id=entrepreneur_model.person_id,
            name=entrepreneur_model.name,
            registration_number=RegistrationNumber(entrepreneur_model.registration_number),
            vat_number=VatNumber(entrepreneur_model.vat_number) if entrepreneur_model.vat_number else None,
            is_vat_payer=entrepreneur_model.is_vat_payer,
            phone_id=entrepreneur_model.phone_id,
            email_id=entrepreneur_model.email_id,
        )
