from app.application.dto.address.retrieve_address import RetrieveAddressOut
from app.domain.addresses.repositories.address import AddressRepository


class RetrieveAddresses:

    def __init__(self, address_repository: AddressRepository) -> None:
        """
        Initialize use-case

        Args:
            address_repository: Address repository
        """
        self.address_repository = address_repository

    def execute(self) -> list[RetrieveAddressOut]:
        """
        Retrieve all addresses

        Returns:
            List of all addresses
        """
        addresses = self.address_repository.get_all()

        return [
            RetrieveAddressOut(
                id=address.id,
                external_id=address.external_id,
                street=address.street,
                building_number=address.building_number,
                orientation_number=address.orientation_number,
                orientation_number_letter=address.orientation_number_letter,
                district=address.district,
                city=address.city,
                postal_code=address.postal_code,
                country_id=address.country_id,
            )
            for address in addresses
        ]

