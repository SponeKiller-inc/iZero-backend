from app.domain.users.entities import user_role
from app.domain.shared.value_objects.period import ValidityPeriod
from datetime import datetime
from app.infrastructure.repositories.base import BaseAlchemyRepository
from app.infrastructure.models.user.user_modules import UserModuleModel
from app.domain.users.entities.user_module import UserModule

class AlchemyUserModuleRepository(BaseAlchemyRepository):

    def get(self, user_id, ref_date: datetime) -> list[UserModule]:
        """
        Get all user modules by user ID
        
        Args:
            user_id: User ID
            ref_date: Reference date
        
        Returns:
            List of user modules
        """

        user_module_model = (
            self.db
                .query(UserModuleModel)
                .filter(
                    UserModuleModel.user_id == user_id,
                    UserModuleModel.valid_at(ref_date),
                )
                .all()
        )

        return [
            UserModule(
                id=user_module.id,
                user_id=user_module.user_id,
                module_id=user_module.module_id,
                validity=ValidityPeriod(
                    valid_from=user_module.valid_from,
                    valid_to=user_module.valid_to,
                )
            )
            for user_module in user_module_model
        ]

    def get_module(
        self, 
        user_id: int, 
        module_id: int, 
        ref_date: datetime
    ) -> UserModule | None:
        """
        Get user module
        
        Args:
            user_id: User ID
            module_id: Module ID
            ref_date: Reference date
        
        Returns:
            User module entity
        """

        user_module_model = (
            self.db
                .query(UserModuleModel)
                .filter(
                    UserModuleModel.user_id == user_id,
                    UserModuleModel.module_id == module_id,
                    UserModuleModel.valid_at(ref_date),
                )
                .first()
        )

        if not user_module_model:
            return None

        return UserModule(
            id=user_module_model.id,
            user_id=user_module_model.user_id,
            module_id=user_module_model.module_id,
            validity=ValidityPeriod(
                valid_from=user_module_model.valid_from,
                valid_to=user_module_model.valid_to,
            )
        )

    def save(self, user_module: UserModule) -> UserModule:
        """
        Save user module
        
        Args:
            user_module: User module entity
        
        Returns:
            User module entity
        """

        if user_module.id is None:
            return self._insert(user_module)
        else:
            return self._update(user_module)

    def _insert(self, user_module: UserModule) -> UserModule:
        """
        Insert user module
        
        Args:
            user_module: User module entity
        
        Returns:
            User module entity
        """

        user_module_model = UserModuleModel(
            id=user_module.id,
            user_id=user_module.user_id,
            module_id=user_module.module_id,
            valid_from=user_module.validity.valid_from,
            valid_to=user_module.validity.valid_to,
        )

        self.db.add(user_module_model)
        self.db.commit()
        self.db.refresh(user_module_model)

        return UserModule(
            id=user_module_model.id,
            user_id=user_module_model.user_id,
            module_id=user_module_model.module_id,
            validity=ValidityPeriod(
                valid_from=user_module_model.valid_from,
                valid_to=user_module_model.valid_to,
            )
        )

    def _update(self, user_module: UserModule) -> UserModule:
        """
        Update user module
        
        Args:
            user_module: User module entity
        
        Returns:
            User module entity
        """

        user_module_model = (
            self.db
                .query(UserModuleModel)
                .filter(UserModuleModel.id == user_module.id)
                .first()
        )

        user_module_model.user_id = user_module.user_id
        user_module_model.module_id = user_module.module_id
        user_module_model.valid_from = user_module.validity.valid_from
        user_module_model.valid_to = user_module.validity.valid_to

        self.db.commit()
        self.db.refresh(user_module_model)

        return UserModule(
            id=user_module_model.id,
            user_id=user_module_model.user_id,
            module_id=user_module_model.module_id,
            validity=ValidityPeriod(
                valid_from=user_module_model.valid_from,
                valid_to=user_module_model.valid_to,
            )
        )