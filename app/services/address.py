from app.repositories.address import AddressRepository

from app.models.types.addresses import ModelsUnion


class AddressService:
    def __init__(
        self, 
        repo: AddressRepository,
    ):
        self.repo = repo
        
    def retrieve_all_addresses(
        self,
        user_id: int,
        customer_id: int
    ) -> ModelsUnion:
        
        """
        Retrieve users customer data

        Args:
            user_id (int): user id
            customer_id (int): customer id
        
        Returns:
            Customer: Object 
        
        Raises:
            CustomerNotFoundError - user does not have customer with provided id
            CustomerServiceError - server side error
        """
        try:
            customer = self.repo.get_user_customer(user_id, customer_id)
        
            if customer is None:
                raise CustomerNotFoundError

            return customer
        except SQLAlchemyError as e:
            raise CustomerServiceError("Unable to retrieve customer data") from e

    def retrieve_address(self, address_id: int) -> ModelsUnion:
        try:
            address = self.repo.get_address(address_id)

            if address is None:
                raise AddressNotFoundError

            return address
        except SQLAlchemyError as e:
            raise AddressServiceError("Unable to retrieve address data") from e