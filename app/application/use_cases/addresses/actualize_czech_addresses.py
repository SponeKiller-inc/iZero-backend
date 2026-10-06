from __future__ import annotations

from datetime import date

from app.application.ports.address_provider import AddressProvider
from app.application.use_cases.seed.seed_czech_addresses import CZECH_COUNTRY_CODE
from app.domain.addresses.entities.address import Address
from app.domain.addresses.repositories.address import AddressRepository
from app.domain.addresses.repositories.country import CountryRepository


class ActualizeCzechAddresses:
    """Synchronizes local Czech addresses with the RÚIAN address register:
    fetches addresses modified since a given date and inserts new ones or
    updates existing ones (matched by external ID and country)."""

    def __init__(
        self,
        address_provider: AddressProvider,
        address_repository: AddressRepository,
        country_repository: CountryRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            address_provider: External (RÚIAN) address provider
            address_repository: Address repository
            country_repository: Country repository
        """
        self.address_provider = address_provider
        self.address_repository = address_repository
        self.country_repository = country_repository

    def execute(self, modified_since: date) -> None:
        """
        Fetches Czech addresses modified on or after `modified_since` from the
        address provider and persists them, updating existing addresses
        (matched by external ID and country) or inserting new ones.

        Args:
            modified_since: Only addresses modified on or after this date are
                fetched.

        Raises:
            AddressProviderError: If the external address provider has failed.
        """
        country = self.country_repository.get_by_code(CZECH_COUNTRY_CODE)

        for address_out in self.address_provider.get_modified(modified_since):
            if address_out.country_code.value != CZECH_COUNTRY_CODE:
                continue

            address = self.address_repository.get_by_external_id(
                address_out.external_id, country.id
            )

            if address is None:
                address = Address.create(
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
            else:
                address.street = address_out.street
                address.building_number = address_out.building_number
                address.orientation_number = address_out.orientation_number
                address.orientation_number_letter = (
                    address_out.orientation_number_letter
                )
                address.district = address_out.district
                address.city = address_out.city
                address.postal_code = address_out.postal_code

            self.address_repository.save(address)
