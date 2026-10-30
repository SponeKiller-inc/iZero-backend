from app.application.constants.use_case import UseCase
from app.application.dto.bank.retrieve_bank_account import RetrieveBankAccountOut
from app.application.dto.user.user_bank_account import UserBankAccountIn
from app.application.exceptions.bank import BankAccountAlreadyExistsError
from app.application.security.authorize import authorize
from app.application.use_cases.banks.add_bank_account import AddBankAccount
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.entities.user_bank_account import UserBankAccount
from app.domain.users.repositories.user_bank_account import UserBankAccountRepository


class AddUserBankAccount:

    def __init__(
        self,
        user_bank_account_repository: UserBankAccountRepository,
        add_bank_account: AddBankAccount,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_bank_account_repository: User bank account repository
            add_bank_account: Add bank account use-case
        """
        self.user_bank_account_repository = user_bank_account_repository
        self.add_bank_account = add_bank_account

    @authorize(EntityType.BANK, UseCase.BANKS_ADD_USER_ACCOUNT)
    def execute(self, dto: UserBankAccountIn) -> RetrieveBankAccountOut:
        """
        Add bank account to the user's profile

        Args:
            dto: DTO carrying user id and bank account data

        Returns:
            The added bank account with its bank

        Raises:
            BankAccountAlreadyExistsError: If user already has a bank account
            BankNotFoundError: If bank is not in the catalogue
            BankAccountValidationError: If account prefix, account number or IBAN
                has invalid format, owner name is empty or IBAN is not a Czech one
        """
        if self.user_bank_account_repository.get(dto.user_id) is not None:
            raise BankAccountAlreadyExistsError("User already has a bank account")

        bank_account = self.add_bank_account.execute(dto.bank_account)

        user_bank_account = UserBankAccount.assign(
            user_id=dto.user_id,
            bank_account_id=bank_account.id,
        )

        self.user_bank_account_repository.save(user_bank_account)

        return bank_account
