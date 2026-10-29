from app.application.constants.use_case import UseCase
from app.application.dto.bank.retrieve_bank_account import RetrieveBankAccountOut
from app.application.dto.bank.retrieve_banks import RetrieveBankOut
from app.application.exceptions.bank import BankAccountNotFoundError, BankNotFoundError
from app.application.security.authorize import authorize
from app.domain.bank.repositories.bank import BankRepository
from app.domain.bank.repositories.bank_account import BankAccountRepository
from app.domain.shared.constants.entity_type import EntityType


class RetrieveBankAccount:

    def __init__(
        self,
        bank_repository: BankRepository,
        bank_account_repository: BankAccountRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            bank_repository: Bank repository
            bank_account_repository: Bank account repository
        """
        self.bank_repository = bank_repository
        self.bank_account_repository = bank_account_repository

    @authorize(EntityType.BANK, UseCase.BANKS_RETRIEVE_ACCOUNT)
    def execute(self, bank_account_id: int) -> RetrieveBankAccountOut:
        """
        Retrieve a bank account with its bank

        Args:
            bank_account_id: Bank account ID

        Returns:
            The bank account with its bank

        Raises:
            BankAccountNotFoundError: If the bank account does not exist
            BankNotFoundError: If the account's bank does not exist
        """
        bank_account = self.bank_account_repository.get(bank_account_id)

        if bank_account is None:
            raise BankAccountNotFoundError("Bank account does not exist")

        bank = self.bank_repository.get(bank_account.bank_id)

        if bank is None:
            raise BankNotFoundError("Bank does not exist")

        return RetrieveBankAccountOut(
            id=bank_account.id,
            owner_name=bank_account.owner_name,
            account_prefix=bank_account.account_prefix.value,
            account_number=bank_account.account_number.value,
            iban=bank_account.iban.value,
            bank=RetrieveBankOut(
                id=bank.id,
                name=bank.name,
                address_id=bank.address_id,
                code=bank.code.value,
                swift=bank.swift.value,
            ),
        )
