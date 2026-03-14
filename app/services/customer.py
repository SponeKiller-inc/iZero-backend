from app.repositories.user import UserRepository
from app.models.users import Users
from app.models.user_roles import UserRoles
from app.services.google import GoogleAPI
from .constants import SERVICE_CONST
from app.exceptions.domain.user import (
    LocalUserExistsError, 
    GoogleUserExistsError, 
    UserExistsError, 
    RegistrationError,
)
from app.exceptions.repository.user import (
    UserRoleNotAddedError,
)
from app.exceptions.domain.google import GoogleAuthError
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
)
from app.exceptions.infrastucture.domain import UserServiceError

from app.utils import utils


class CustomerService:
    def __init__(
        self, 
        repo: CustomerRepository,
        user_service: UserService
    ):
        self.repo = repo
        self.user_service = user_service
        
    def retrieve_customer_data(
        self,
        user_id: int,
        customer_id: int
    ) -> Customer:
        
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