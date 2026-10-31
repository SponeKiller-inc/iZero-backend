from app.domain.persons.entities.company import Company
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)
from app.infrastructure.models.person.companies import CompanyModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyCompanyRepository(BaseAlchemyRepository):
    def get_by_person_id(self, person_id: int) -> Company | None:
        """
        Get company details by person ID

        Args:
            person_id: Person ID

        Returns:
            Company entity if found, else None
        """

        company_model = (
            self.db
                .query(CompanyModel)
                .filter(CompanyModel.person_id == person_id)
                .first()
        )

        if company_model is None:
            return None

        return self._to_entity(company_model)

    def get_by_registration_number(self, registration_number: str) -> Company | None:
        """
        Get company details by company registration number

        Args:
            registration_number: Company registration number

        Returns:
            Company entity if found, else None
        """

        company_model = (
            self.db
                .query(CompanyModel)
                .filter(CompanyModel.registration_number == registration_number)
                .first()
        )

        if company_model is None:
            return None

        return self._to_entity(company_model)

    def save(self, company: Company) -> Company:
        """
        Save new or existing company details

        Args:
            company: Company entity to save

        Returns:
            Saved company entity
        """

        if company.id is None:
            return self._insert(company)
        else:
            return self._update(company)

    def _insert(self, company: Company) -> Company:
        company_model = CompanyModel(
            person_id=company.person_id,
            name=company.name,
            legal_form_id=company.legal_form_id,
            registration_number=company.registration_number.value,
            vat_number=company.vat_number.value if company.vat_number else None,
            is_vat_payer=company.is_vat_payer,
            representative_person_id=company.representative_person_id,
            phone_id=company.phone_id,
            email_id=company.email_id,
        )
        self.db.add(company_model)
        self.db.flush()
        self.db.refresh(company_model)

        return self._to_entity(company_model)

    def _update(self, company: Company) -> Company:
        company_model = (
            self.db
                .query(CompanyModel)
                .filter(CompanyModel.id == company.id)
                .first()
        )

        company_model.name = company.name
        company_model.legal_form_id = company.legal_form_id
        company_model.registration_number = company.registration_number.value
        company_model.vat_number = company.vat_number.value if company.vat_number else None
        company_model.is_vat_payer = company.is_vat_payer
        company_model.representative_person_id = company.representative_person_id
        company_model.phone_id = company.phone_id
        company_model.email_id = company.email_id

        self.db.flush()
        self.db.refresh(company_model)

        return self._to_entity(company_model)

    def _to_entity(self, company_model: CompanyModel) -> Company:
        return Company(
            id=company_model.id,
            person_id=company_model.person_id,
            name=company_model.name,
            legal_form_id=company_model.legal_form_id,
            registration_number=RegistrationNumber(company_model.registration_number),
            vat_number=VatNumber(company_model.vat_number) if company_model.vat_number else None,
            is_vat_payer=company_model.is_vat_payer,
            representative_person_id=company_model.representative_person_id,
            phone_id=company_model.phone_id,
            email_id=company_model.email_id,
        )
