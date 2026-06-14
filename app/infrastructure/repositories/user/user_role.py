from app.infrastructure.models.user.users import UserModel
from app.domain.users.entities.user_role import UserRole
from app.domain.shared.constants.role_type import RoleType
from app.infrastructure.models.user.user_roles import UserRoleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyUserRoleRepository(BaseAlchemyRepository):
    def get_user_role(self, user_id: int, role: RoleType) -> UserRole | None:

        user_role_model = (
            self.db
                .query(UserRoleModel)
                .filter(
                    UserRoleModel.user_id == user_id,
                    UserRoleModel.role == role,
                )
                .first()
        )

        if user_role_model is None:
            return None
        
        return UserRole(
            id=user_role_model.id,
            user_id=user_role_model.user_id,
            role=user_role_model.role,
        )   
    
    def save(self, user_role: UserRole) -> UserRole:
        """
        Create or update User role

        Args:
            user_role (UserRole): data to create or update user_role
        
        Returns:
            UserRole: data newly created or updated user_role
        """
         
        if user_role.id is None:
            return self._insert(user_role)
        else:
            return self._update(user_role)

    def _insert(self, user_role: UserRole) -> UserRole:
        """
        Create user role

        Args:
            user_role (UserRole) - data to create user_role
        
        Returns:
            UserRole: data newly created user_role
        """
               
        user_model = UserRoleModel(
            user_id=user_role.user_id,
            role=user_role.role,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return UserRole(
            id=user_model.id,
            user_id=user_model.user_id,
            role=user_model.role,
        )

    def _update(self, user_role: UserRole) -> UserRole:
        """
        Update user role

        Args:
            user_role (UserRole) - data to update user_role
        
        Returns:
            UserRole: data updated user_role
        """

        updated_user_role = (
            self.db
                .query(UserRoleModel)
                .filter(UserRoleModel.id == user_role.id)
                .first()      
        )

        updated_user_role.user_id = user_role.user_id
        updated_user_role.role = user_role.role

        self.db.commit()
        self.db.refresh(updated_user_role)

        return UserRole(
            id=updated_user_role.id,
            user_id=updated_user_role.user_id,
            role=updated_user_role.role, 
        )