from app.application.seed_data.phone_prefixes import PHONE_PREFIXES
from app.domain.addresses.repositories.country import CountryRepository
from app.domain.shared.entities.phone_prefix import PhonePrefix
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository


class SeedDefaultPhonePrefixes:
    """Ensures the catalogue of phone prefixes is created"""

    def __init__(
        self,
        phone_prefix_repository: PhonePrefixRepository,
        country_repository: CountryRepository,
    ) -> None:
        self.phone_prefix_repository = phone_prefix_repository
        self.country_repository = country_repository

    def execute(self) -> None:
        """
        Inserts missing phone prefixes and overwrites the country of existing ones.
        The countries must be seeded first.
        """
        for prefix, country_code in PHONE_PREFIXES:
            country = self.country_repository.get_by_code(country_code)
            phone_prefix = self.phone_prefix_repository.get_by_prefix(prefix)

            if phone_prefix is None:
                phone_prefix = PhonePrefix.create(prefix=prefix, country_id=country.id)
            else:
                phone_prefix.update(prefix=prefix, country_id=country.id)

            self.phone_prefix_repository.save(phone_prefix)
