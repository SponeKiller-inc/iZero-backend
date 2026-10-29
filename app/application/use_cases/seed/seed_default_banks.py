from app.application.exceptions.address import AddressNotFoundError
from app.application.seed_data.banks import BANKS
from app.domain.addresses.repositories.address import AddressRepository
from app.domain.addresses.repositories.country import CountryRepository
from app.domain.bank.entities.bank import Bank
from app.domain.bank.repositories.bank import BankRepository
from app.domain.bank.value_objects.bank_identification import BankCode, Swift
from app.domain.shared.value_objects.identification import RegistrationNumber


class SeedDefaultBanks:
    """Ensures the bank catalogue is created"""

    def __init__(
        self,
        bank_repository: BankRepository,
        address_repository: AddressRepository,
        country_repository: CountryRepository,
    ) -> None:
        self.bank_repository = bank_repository
        self.address_repository = address_repository
        self.country_repository = country_repository

    def execute(self) -> None:
        """
        Inserts missing banks and overwrites existing ones. The seat address
        is resolved by its RÚIAN address point code, so the Czech addresses
        must be seeded first.

        Raises:
            AddressNotFoundError: If the seat address of a bank does not exist.
        """
        country = self.country_repository.get_by_code("CZE")

        for code, name, swift, registration_number, tax_number, ruian_code in BANKS:
            address = self.address_repository.get_by_external_id(ruian_code, country.id)

            if address is None:
                raise AddressNotFoundError(
                    f"Address {ruian_code} of bank {code} does not exist"
                )

            bank = self.bank_repository.get_by_code(code)

            if bank is None:
                bank = Bank.create(
                    name=name,
                    address_id=address.id,
                    code=BankCode(code),
                    swift=Swift(swift),
                    registration_number=RegistrationNumber(registration_number),
                    tax_number=tax_number,
                )
            else:
                bank.update(
                    name=name,
                    address_id=address.id,
                    swift=Swift(swift),
                    registration_number=RegistrationNumber(registration_number),
                    tax_number=tax_number,
                )

            self.bank_repository.save(bank)
