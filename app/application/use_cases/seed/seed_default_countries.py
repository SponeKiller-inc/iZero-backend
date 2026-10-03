from app.domain.addresses.constants.countries import COUNTRIES
from app.domain.addresses.entities.country import Country
from app.domain.addresses.repositories.country import CountryRepository
from app.domain.shared.value_objects.location import CountryIsoCode


class SeedDefaultCountries:
    """Ensures all ISO 3166-1 alpha-3 countries exist, inserting any that are missing."""

    def __init__(self, country_repository: CountryRepository) -> None:
        self.country_repository = country_repository

    def execute(self) -> None:
        for code, name in COUNTRIES:
            if self.country_repository.get_by_code(code) is None:
                self.country_repository.save(
                    Country.create(code=CountryIsoCode(code), name=name)
                )
