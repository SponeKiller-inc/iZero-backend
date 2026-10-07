from datetime import date
from typing import Protocol

from app.application.dto.address.address_provider import AddressProviderOut


class AddressProvider(Protocol):
    def get_all(self) -> list[AddressProviderOut]:
        """
        Retrieve all addresses from the external address provider.

        Returns:
            AddressProviderOut: All addresses known to the provider.

        Raises:
            AddressProviderError: If the address provider has failed.
        """
        ...

    def get_modified(self, since: date) -> list[AddressProviderOut]:
        """
        Retrieve addresses that were modified since the given date.

        Args:
            since: Only addresses modified on or after this date are returned.

        Returns:
            AddressProviderOut: Addresses modified on or after `since`.

        Raises:
            AddressProviderError: If the address provider has failed.
        """
        ...
