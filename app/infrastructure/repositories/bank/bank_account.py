from app.domain.bank.entities.bank_account import BankAccount
from app.domain.bank.value_objects.bank_identification import (
    AccountNumber,
    AccountPrefix,
    Iban,
)
from app.infrastructure.models.bank.bank_accounts import BankAccountModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyBankAccountRepository(BaseAlchemyRepository):
    def get(self, bank_account_id: int) -> BankAccount | None:
        """
        Get bank account by ID

        Args:
            bank_account_id: Bank account ID

        Returns:
            BankAccount entity if found, else None
        """

        bank_account_model = (
            self.db
                .query(BankAccountModel)
                .filter(BankAccountModel.id == bank_account_id)
                .first()
        )

        if bank_account_model is None:
            return None

        return self._to_entity(bank_account_model)

    def save(self, bank_account: BankAccount) -> BankAccount:
        """
        Save new or existing bank account

        Args:
            bank_account: BankAccount entity to save

        Returns:
            Saved bank account entity
        """

        if bank_account.id is None:
            return self._insert(bank_account)
        else:
            return self._update(bank_account)

    def _insert(self, bank_account: BankAccount) -> BankAccount:
        bank_account_model = BankAccountModel(
            bank_id=bank_account.bank_id,
            owner_name=bank_account.owner_name,
            account_prefix=bank_account.account_prefix.value,
            account_number=bank_account.account_number.value,
            iban=bank_account.iban.value,
        )
        self.db.add(bank_account_model)
        self.db.flush()
        self.db.refresh(bank_account_model)

        return self._to_entity(bank_account_model)

    def _update(self, bank_account: BankAccount) -> BankAccount:
        bank_account_model = (
            self.db
                .query(BankAccountModel)
                .filter(BankAccountModel.id == bank_account.id)
                .first()
        )

        bank_account_model.bank_id = bank_account.bank_id
        bank_account_model.owner_name = bank_account.owner_name
        bank_account_model.account_prefix = bank_account.account_prefix.value
        bank_account_model.account_number = bank_account.account_number.value
        bank_account_model.iban = bank_account.iban.value

        self.db.flush()
        self.db.refresh(bank_account_model)

        return self._to_entity(bank_account_model)

    @staticmethod
    def _to_entity(bank_account_model: BankAccountModel) -> BankAccount:
        return BankAccount(
            id=bank_account_model.id,
            bank_id=bank_account_model.bank_id,
            owner_name=bank_account_model.owner_name,
            account_prefix=AccountPrefix(bank_account_model.account_prefix),
            account_number=AccountNumber(bank_account_model.account_number),
            iban=Iban(bank_account_model.iban),
        )
