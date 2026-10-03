from app.domain.addresses.constants.address_type import (
    ADDRESS_TYPE_MAILING_DESCRIPTION,
    ADDRESS_TYPE_MAILING_ID,
    ADDRESS_TYPE_PERMANENT_DESCRIPTION,
    ADDRESS_TYPE_PERMANENT_ID,
)
from app.domain.addresses.entities.address_type import AddressType
from app.domain.addresses.repositories.address_type import AddressTypeRepository


class SeedDefaultAddressTypes:
    """Ensures the fixed permanent/mailing address-type rows exist under their fixed IDs."""

    def __init__(self, address_type_repository: AddressTypeRepository) -> None:
        self.address_type_repository = address_type_repository

    def execute(self) -> None:
        for address_type_id, description in (
            (ADDRESS_TYPE_PERMANENT_ID, ADDRESS_TYPE_PERMANENT_DESCRIPTION),
            (ADDRESS_TYPE_MAILING_ID, ADDRESS_TYPE_MAILING_DESCRIPTION),
        ):
            if self.address_type_repository.get(address_type_id) is None:
                self.address_type_repository.save(
                    AddressType(id=address_type_id, description=description)
                )
