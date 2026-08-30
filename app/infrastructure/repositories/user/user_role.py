from datetime import datetime

from app.domain.users.entities.user_role import UserRole
from app.domain.shared.value_objects.period import ValidityPeriod
from app.infrastructure.models.user.user_roles import UserRoleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyUserRoleRepository(BaseAlchemyRepository):
    def get(self, user_id: int, ref_date: datetime) -> list[UserRole]:

        user_role_models = (
            self.db
                .query(UserRoleModel)
                .filter(
                    UserRoleModel.user_id == user_id,
                    UserRoleModel.valid_at(ref_date)
                )
                .all()
        )

        if not user_role_models:
            return []
        
        return [
            self._to_entity(user_role)
            for user_role in user_role_models
        ]
    
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
            role_id=user_role.role_id,
            valid_from=user_role.validity.valid_from,
            valid_to=user_role.validity.valid_to,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return self._to_entity(user_model)

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
        updated_user_role.role_id = user_role.role_id
        updated_user_role.valid_from = user_role.validity.valid_from
        updated_user_role.valid_to = user_role.validity.valid_to

        self.db.commit()
        self.db.refresh(updated_user_role)

        return self._to_entity(updated_user_role)

    @staticmethod
    def _to_entity(user_role_model: UserRoleModel) -> UserRole:
        return UserRole(
            id=user_role_model.id,
            user_id=user_role_model.user_id,
            role_id=user_role_model.role_id,
            validity=ValidityPeriod(
                valid_from=user_role_model.valid_from,
                valid_to=user_role_model.valid_to,
            ),
        )