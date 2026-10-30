from app.application.constants.use_case import UseCase
from app.application.dto.bank.retrieve_bank_account import RetrieveBankAccountOut
from app.application.security.authorize import authorize
from app.application.use_cases.banks.retrieve_bank_account import RetrieveBankAccount
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.repositories.user_bank_account import UserBankAccountRepository


class RetrieveUserBankAccount:

    def __init__(
        self,
        user_bank_account_repository: UserBankAccountRepository,
        retrieve_bank_account: RetrieveBankAccount,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_bank_account_repository: User bank account repository
            retrieve_bank_account: Retrieve bank account use-case
        """
        self.user_bank_account_repository = user_bank_account_repository
        self.retrieve_bank_account = retrieve_bank_account

    @authorize(EntityType.BANK, UseCase.BANKS_RETRIEVE_USER_ACCOUNT)
    def execute(self, user_id: int) -> RetrieveBankAccountOut | None:
        """
        Retrieve the user's bank account with its bank

        Args:
            user_id: User ID

        Returns:
            The user's bank account, None if user has no bank account

        Raises:
            BankAccountNotFoundError: If the assigned bank account does not exist
            BankNotFoundError: If the account's bank does not exist
        """
        user_bank_account = self.user_bank_account_repository.get(user_id)

        if user_bank_account is None:
            return None

        return self.retrieve_bank_account.execute(user_bank_account.bank_account_id)
