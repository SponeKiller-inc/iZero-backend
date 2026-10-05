from app.application.exceptions.address import CountryNotFoundError
from app.application.ports.address_provider import AddressProvider
from app.domain.addresses.entities.address import Address
from app.domain.addresses.repositories.address import AddressRepository
from app.domain.addresses.repositories.country import CountryRepository

# ISO 3166-1 alpha-3 code of the Czech Republic, as used throughout the
# address catalogue.
CZECH_COUNTRY_CODE = "CZE"


class SeedCzechAddresses:
    """Imports the full Czech (e.g. RÚIAN) address catalogue from the
    external address provider. Addresses are immutable reference data that
    only need to be populated once, at application setup; if Czech
    addresses already exist, the import is skipped entirely."""

    def __init__(
        self,
        address_provider: AddressProvider,
        address_repository: AddressRepository,
        country_repository: CountryRepository,
    ) -> None:
        self.address_provider = address_provider
        self.address_repository = address_repository
        self.country_repository = country_repository

    def execute(self) -> None:
        """
        Downloads all Czech addresses from the provider and persists them.

        No-ops if Czech addresses have already been imported.

        Raises:
            CountryNotFoundError: If Czechia hasn't been seeded yet.
            AddressProviderError: If the external address provider has failed.
        """
        country = self.country_repository.get_by_code(CZECH_COUNTRY_CODE)
        if country is None or country.id is None:
            raise CountryNotFoundError(
                "Czechia must be seeded before Czech addresses can be imported."
            )

        if self.address_repository.exists_for_country(country.id):
            return

        for address_out in self.address_provider.get_all():
            if address_out.country_code.value != CZECH_COUNTRY_CODE:
                continue

            self.address_repository.save(
                Address.create(
                    external_id=address_out.external_id,
                    street=address_out.street,
                    building_number=address_out.building_number,
                    orientation_number=address_out.orientation_number,
                    orientation_number_letter=address_out.orientation_number_letter,
                    district=address_out.district,
                    city=address_out.city,
                    postal_code=address_out.postal_code,
                    country_id=country.id,
                )
            )
