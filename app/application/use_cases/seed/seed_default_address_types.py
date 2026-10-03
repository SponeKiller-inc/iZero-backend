from app.domain.addresses.constants.address_type import (
    ADDRESS_TYPE_MAILING_DESCRIPTION,
    ADDRESS_TYPE_MAILING_TYPE,
    ADDRESS_TYPE_PERMANENT_DESCRIPTION,
    ADDRESS_TYPE_PERMANENT_TYPE,
)
from app.domain.addresses.entities.address_type import AddressType
from app.domain.addresses.repositories.address_type import (
    AddressTypeRepository,
)


class SeedDefaultAddressTypes:
    """Ensures the permanent/mailing address-type rows exist, keyed by
    their type."""

    def __init__(self, address_type_repository: AddressTypeRepository) -> None:
        self.address_type_repository = address_type_repository

    def execute(self) -> None:
        for type_, description in (
            (ADDRESS_TYPE_PERMANENT_TYPE, ADDRESS_TYPE_PERMANENT_DESCRIPTION),
            (ADDRESS_TYPE_MAILING_TYPE, ADDRESS_TYPE_MAILING_DESCRIPTION),
        ):
            if self.address_type_repository.get_by_type(type_) is None:
                self.address_type_repository.save(
                    AddressType.create(type=type_, description=description)
                )
