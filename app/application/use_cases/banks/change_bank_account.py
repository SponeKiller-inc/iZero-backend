from app.application.constants.use_case import UseCase
from app.application.dto.bank.bank_account import BankAccountIn
from app.application.dto.bank.retrieve_bank_account import RetrieveBankAccountOut
from app.application.exceptions.bank import (
    BankAccountNotFoundError,
    BankAccountValidationError,
    BankNotFoundError,
)
from app.application.security.authorize import authorize
from app.application.use_cases.banks.retrieve_bank_account import RetrieveBankAccount
from app.domain.bank.exceptions import bank_account as bank_account_errors
from app.domain.bank.repositories.bank import BankRepository
from app.domain.bank.repositories.bank_account import BankAccountRepository
from app.domain.bank.value_objects.bank_identification import (
    AccountNumber,
    AccountPrefix,
    Iban,
)
from app.domain.shared.constants.entity_type import EntityType


class ChangeBankAccount:

    def __init__(
        self,
        bank_repository: BankRepository,
        bank_account_repository: BankAccountRepository,
        retrieve_bank_account: RetrieveBankAccount,
    ) -> None:
        """
        Initialize use-case

        Args:
            bank_repository: Bank repository
            bank_account_repository: Bank account repository
            retrieve_bank_account: Retrieve bank account use-case
        """
        self.bank_repository = bank_repository
        self.bank_account_repository = bank_account_repository
        self.retrieve_bank_account = retrieve_bank_account

    @authorize(EntityType.BANK, UseCase.BANKS_CHANGE_ACCOUNT)
    def execute(self, bank_account_id: int, dto: BankAccountIn) -> RetrieveBankAccountOut:
        """
        Change details of a bank account

        Args:
            bank_account_id: Bank account ID
            dto: DTO carrying changed bank account data

        Returns:
            The changed bank account with its bank

        Raises:
            BankAccountNotFoundError: If the bank account does not exist
            BankNotFoundError: If bank is not in the catalogue
            BankAccountValidationError: If account prefix, account number or IBAN
                has invalid format, owner name is empty or IBAN is not a Czech one
        """
        bank_account = self.bank_account_repository.get(bank_account_id)

        if bank_account is None:
            raise BankAccountNotFoundError("Bank account does not exist")

        bank = self.bank_repository.get(dto.bank_id)

        if bank is None:
            raise BankNotFoundError("Bank does not exist")

        try:
            account_prefix = AccountPrefix(dto.account_prefix)
            account_number = AccountNumber(dto.account_number)
            iban = Iban(dto.iban)
            bank_account.update(
                bank=bank,
                owner_name=dto.owner_name,
                account_prefix=account_prefix,
                account_number=account_number,
                iban=iban,
            )
        except (ValueError, bank_account_errors.BankAccountValidationError) as e:
            raise BankAccountValidationError(str(e)) from e

        self.bank_account_repository.save(bank_account)

        return self.retrieve_bank_account.execute(bank_account_id)
