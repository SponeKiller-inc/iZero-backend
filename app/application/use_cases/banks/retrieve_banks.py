from app.application.constants.use_case import UseCase
from app.application.dto.bank.retrieve_banks import RetrieveBankOut
from app.application.security.authorize import authorize
from app.domain.bank.repositories.bank import BankRepository
from app.domain.shared.constants.entity_type import EntityType


class RetrieveBanks:

    def __init__(self, bank_repository: BankRepository) -> None:
        """
        Initialize use-case

        Args:
            bank_repository: Bank repository
        """
        self.bank_repository = bank_repository

    @authorize(EntityType.BANK, UseCase.BANKS_RETRIEVE)
    def execute(self) -> list[RetrieveBankOut]:
        """
        Retrieve all banks of the catalogue

        Returns:
            List of all banks, empty if the catalogue is empty
        """
        return [
            RetrieveBankOut(
                id=bank.id,
                name=bank.name,
                address_id=bank.address_id,
                code=bank.code.value,
                swift=bank.swift.value,
            )
            for bank in self.bank_repository.get_all()
        ]
