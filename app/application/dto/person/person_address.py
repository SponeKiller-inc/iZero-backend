from dataclasses import dataclass

from app.application.dto.address.retrieve_address import RetrieveAddressOut


@dataclass(frozen=True)
class AddressIn:
    """DTO carrying one address of a person with its type."""
    address_id: int
    address_type_id: int

@dataclass(frozen=True)
class PersonAddressIn:
    """
    Input DTO for AssignPersonAddress use-case.
    """
    person_id: int
    addresses: list[AddressIn]

@dataclass(frozen=True)
class PersonAddressOut:
    """DTO carrying an address currently assigned to a person with its type."""
    id: int
    address_type: str
    address: RetrieveAddressOut
