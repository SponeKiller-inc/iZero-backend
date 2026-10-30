from app.application.constants.use_case import UseCase
from app.application.dto.bank.retrieve_bank_account import RetrieveBankAccountOut
from app.application.dto.user.user_bank_account import UserBankAccountIn
from app.application.exceptions.bank import BankAccountNotFoundError
from app.application.security.authorize import authorize
from app.application.use_cases.banks.change_bank_account import ChangeBankAccount
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.repositories.user_bank_account import UserBankAccountRepository


class ChangeUserBankAccount:

    def __init__(
        self,
        user_bank_account_repository: UserBankAccountRepository,
        change_bank_account: ChangeBankAccount,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_bank_account_repository: User bank account repository
            change_bank_account: Change bank account use-case
        """
        self.user_bank_account_repository = user_bank_account_repository
        self.change_bank_account = change_bank_account

    @authorize(EntityType.BANK, UseCase.BANKS_CHANGE_USER_ACCOUNT)
    def execute(self, dto: UserBankAccountIn) -> RetrieveBankAccountOut:
        """
        Change details of the user's bank account

        Args:
            dto: DTO carrying user id and changed bank account data

        Returns:
            The changed bank account with its bank

        Raises:
            BankAccountNotFoundError: If user has no bank account
            BankNotFoundError: If bank is not in the catalogue
            BankAccountValidationError: If account prefix, account number or IBAN
                has invalid format, owner name is empty or IBAN is not a Czech one
        """
        user_bank_account = self.user_bank_account_repository.get(dto.user_id)

        if user_bank_account is None:
            raise BankAccountNotFoundError("User has no bank account")

        return self.change_bank_account.execute(
            user_bank_account.bank_account_id,
            dto.bank_account,
        )
