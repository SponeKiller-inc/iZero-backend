from app.domain.bank.entities.bank import Bank
from app.domain.bank.value_objects.bank_identification import BankCode, Swift
from app.domain.shared.value_objects.identification import RegistrationNumber
from app.infrastructure.models.bank.banks import BankModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyBankRepository(BaseAlchemyRepository):
    def get(self, bank_id: int) -> Bank | None:
        """
        Get bank by ID

        Args:
            bank_id: Bank ID

        Returns:
            Bank entity if found, else None
        """

        bank_model = (
            self.db
                .query(BankModel)
                .filter(BankModel.id == bank_id)
                .first()
        )

        if bank_model is None:
            return None

        return self._to_entity(bank_model)

    def get_by_code(self, code: str) -> Bank | None:
        """
        Get bank by its national bank code

        Args:
            code: National bank code

        Returns:
            Bank entity if found, else None
        """

        bank_model = (
            self.db
                .query(BankModel)
                .filter(BankModel.code == code)
                .first()
        )

        if bank_model is None:
            return None

        return self._to_entity(bank_model)

    def get_all(self) -> list[Bank]:
        """
        Get all banks of the catalogue

        Returns:
            List of Bank entities
        """

        return [
            self._to_entity(bank_model)
            for bank_model in self.db.query(BankModel).order_by(BankModel.code).all()
        ]

    def save(self, bank: Bank) -> Bank:
        """
        Save new or existing bank

        Args:
            bank: Bank entity to save

        Returns:
            Saved bank entity
        """

        if bank.id is None:
            return self._insert(bank)
        else:
            return self._update(bank)

    def _insert(self, bank: Bank) -> Bank:
        bank_model = BankModel(
            name=bank.name,
            address_id=bank.address_id,
            code=bank.code.value,
            swift_code=bank.swift.value,
            registration_number=bank.registration_number.value,
            tax_number=bank.tax_number,
        )
        self.db.add(bank_model)
        self.db.flush()
        self.db.refresh(bank_model)

        return self._to_entity(bank_model)

    def _update(self, bank: Bank) -> Bank:
        bank_model = (
            self.db
                .query(BankModel)
                .filter(BankModel.id == bank.id)
                .first()
        )

        bank_model.name = bank.name
        bank_model.address_id = bank.address_id
        bank_model.code = bank.code.value
        bank_model.swift_code = bank.swift.value
        bank_model.registration_number = bank.registration_number.value
        bank_model.tax_number = bank.tax_number

        self.db.flush()
        self.db.refresh(bank_model)

        return self._to_entity(bank_model)

    @staticmethod
    def _to_entity(bank_model: BankModel) -> Bank:
        return Bank(
            id=bank_model.id,
            name=bank_model.name,
            address_id=bank_model.address_id,
            code=BankCode(bank_model.code),
            swift=Swift(bank_model.swift_code),
            registration_number=RegistrationNumber(bank_model.registration_number),
            tax_number=bank_model.tax_number,
        )
