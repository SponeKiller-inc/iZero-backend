from app.repositories.address import AddressRepository
from app.models.types.addresses import AddressesUnion


class AddressService:
    def __init__(
        self, 
        repo: AddressRepository,
    ):
        self.repo = repo
        
    def retrieve_all_addresses(self) -> dict[str, list[AddressesUnion]] | []:
        
        """
        Retrieve all addresses
        
        Returns:
            dict[str, list[AddressesUnion]] or []:  dictionary of addresses 
                or empty list if no addresses found
        """

        address_registry = self.repo.get_all_available_countries()

        addresses = {}

        for country in address_registry:
            address_repository = getattr(
                self.repo, "get_all" + country.table_name
            )
            addresses[country.country_code] = address_repository()

        return addresses
        
    def retrieve_address(self, address_id: int) -> AddressesUnion | None:
        """
        Retrieve address data

        Args:
            address_id (int): address id
        
        Returns:
            Proper Address object or None
        """
        country_code = self.repo.get_country_code(address_id)

        if country_code is None:
            return None

        address_registry = self.repo.get_available_country(country_code)

        if address_registry is None:
            return None

        address_repository = getattr(
            self.repo, "get_" + address_registry.table_name
        )

        return address_repository(address_id)
