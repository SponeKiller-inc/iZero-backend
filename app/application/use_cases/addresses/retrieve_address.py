from app.application.dto.address.retrieve_address import RetrieveAddressOut
from app.application.exceptions.address import AddressNotFoundError
from app.domain.addresses.repositories.address import AddressRepository


class RetrieveAddress:

    def __init__(self, address_repository: AddressRepository) -> None:
        """
        Initialize use-case

        Args:
            address_repository: Address repository
        """
        self.address_repository = address_repository

    def execute(self, address_id: int) -> RetrieveAddressOut:
        """
        Retrieve an address by its ID

        Args:
            address_id: Address ID

        Returns:
            The retrieved address

        Raises:
            AddressNotFoundError: If the address does not exist
        """
        address = self.address_repository.get(address_id)

        if address is None:
            raise AddressNotFoundError("Address does not exist")

        return RetrieveAddressOut(
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

