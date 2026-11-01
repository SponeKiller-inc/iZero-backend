from dataclasses import dataclass

from app.application.dto.address.retrieve_address import RetrieveAddressOut


@dataclass(frozen=True)
class PersonAddressIn:
    """
    Input DTO for AssignPersonAddress use-case.
    """
    address_id: int
    address_type: str

@dataclass(frozen=True)
class PersonAddressOut:
    """DTO carrying an address currently assigned to a person with its type."""
    id: int
    address_type: str
    address: RetrieveAddressOut
