from app.domain.users.entities.user_bank_account import UserBankAccount
from app.infrastructure.models.user.user_bank_accounts import UserBankAccountModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyUserBankAccountRepository(BaseAlchemyRepository):
    def get(self, user_id: int) -> UserBankAccount | None:
        """
        Get bank account assignment of the user

        Args:
            user_id: User ID

        Returns:
            UserBankAccount entity if found, else None
        """

        user_bank_account_model = (
            self.db
                .query(UserBankAccountModel)
                .filter(UserBankAccountModel.user_id == user_id)
                .first()
        )

        if user_bank_account_model is None:
            return None

        return self._to_entity(user_bank_account_model)

    def save(self, user_bank_account: UserBankAccount) -> UserBankAccount:
        """
        Save new or existing bank account assignment

        Args:
            user_bank_account: UserBankAccount entity to save

        Returns:
            Saved user bank account entity
        """

        if user_bank_account.id is None:
            return self._insert(user_bank_account)
        else:
            return self._update(user_bank_account)

    def _insert(self, user_bank_account: UserBankAccount) -> UserBankAccount:
        user_bank_account_model = UserBankAccountModel(
            user_id=user_bank_account.user_id,
            bank_account_id=user_bank_account.bank_account_id,
        )
        self.db.add(user_bank_account_model)
        self.db.flush()
        self.db.refresh(user_bank_account_model)

        return self._to_entity(user_bank_account_model)

    def _update(self, user_bank_account: UserBankAccount) -> UserBankAccount:
        user_bank_account_model = (
            self.db
                .query(UserBankAccountModel)
                .filter(UserBankAccountModel.id == user_bank_account.id)
                .first()
        )

        user_bank_account_model.user_id = user_bank_account.user_id
        user_bank_account_model.bank_account_id = user_bank_account.bank_account_id

        self.db.flush()
        self.db.refresh(user_bank_account_model)

        return self._to_entity(user_bank_account_model)

    @staticmethod
    def _to_entity(user_bank_account_model: UserBankAccountModel) -> UserBankAccount:
        return UserBankAccount(
            id=user_bank_account_model.id,
            user_id=user_bank_account_model.user_id,
            bank_account_id=user_bank_account_model.bank_account_id,
        )
