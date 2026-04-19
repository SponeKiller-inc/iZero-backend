from sqlalchemy.orm import Session

from app.models.users import Users
from app.models.user_roles import UserRoles
from app.models.role_types import RoleTypes
from app.exceptions.domain.user import (
    UserExistsError, 
    RegistrationError,
)
from app.exceptions.repository.user import (
    UserRoleNotAddedError,
    UserRoleNotUpdatedError,
)
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
    UpdateExecutionError,
)


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get(self, user_id: int, customer_id: int) -> list[Customers] | None:
        """
        Retrieve user customer data

        Args:
            user_id (int): user id
            customer_id (int): customer id

        Returns:
            Customers or None:  customer data or None if no customer found
        """

        return (
            self.db
                .query(Customers)
                .filter(
                    Customers.id == customer_id,
                    Customers.user_id == user_id
                )
                .first()
        )

        
    

    def get_all(self, user_id: int) -> str | None:
        """
        Get user role

        Args:
            user_id (int): user id

        Returns:
            str or None: user role or None if user not found 
        
        Raises:
            QueryExecutionError - server side error while execution
        """
        
        try:
            return (
                self.db
                    .query(RoleTypes.name)
                    .join(UserRoles, RoleTypes.id == UserRoles.role_type_id)
                    .filter(UserRoles.user_id == user_id)
                    .scalar()
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to get user role") from e
        
    def add(self, new_customer: Customers) -> Customers:
        """
        Add user role

        Args:
            new_user_role (UserRoles): user role data

        Returns:
            UserRoles: newly created user role 
        
        Raises:
            UserRoleNotAddedError - invalid data (user or role not existing) 
            CreateExecutionError - server side error while execution
        """
        
        try:
            self.db.add(new_user_role)
            self.db.commit()
            return new_user_role
        except IntegrityError as e:
            raise UserRoleNotAddedError from e
        except SQLAlchemyError as e:
            raise CreateExecutionError("Failed to add user role") from e
    
    def update(self, user_id: int, role_type_id: int) -> UserRoles:
        """
        Update user role

        Args:
            user_id (int): user id
            role_type_id (int): new user role id

        Returns:
            UserRoles: newly created user role 
        
        Raises:
            UserRoleNotUpdatedError - invalid data (user or role not exists)
            UpdateExecutionError - server side error while execution
        """
        
        try:
            user_role = self.db.query(UserRoles).filter(UserRoles.user_id == user_id).first()
            
            if user_role is None:
                raise UserRoleNotUpdatedError
            
            user_role.role_type_id = role_type_id
            self.db.commit()
            
            return user_role
        except IntegrityError as e:
            raise UserRoleNotUpdatedError from e
        except SQLAlchemyError as e:
            raise UpdateExecutionError("Failed to update user role") from e
            
    
    