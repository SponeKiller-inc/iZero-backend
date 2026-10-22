from collections.abc import Iterator
from datetime import date
from typing import Protocol

from app.application.dto.address.address_provider import AddressProviderOut


class AddressProvider(Protocol):
    def get_all(self) -> Iterator[list[AddressProviderOut]]:
        """
        Retrieve all addresses from the external address provider, one page
        at a time, so callers never hold the whole catalogue in memory.

        Returns:
            Iterator over pages of addresses known to the provider.

        Raises:
            AddressProviderError: If the address provider has failed.
        """
        ...

    def get_modified(self, since: date) -> Iterator[list[AddressProviderOut]]:
        """
        Retrieve addresses that were modified since the given date, one page
        at a time.

        Args:
            since: Only addresses modified on or after this date are returned.

        Returns:
            Iterator over pages of addresses modified on or after `since`.

        Raises:
            AddressProviderError: If the address provider has failed.
        """
        ...
