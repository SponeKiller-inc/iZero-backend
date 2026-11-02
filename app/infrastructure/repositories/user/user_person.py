from app.domain.users.entities.user_person import UserPerson
from app.infrastructure.models.user.user_persons import UserPersonModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyUserPersonRepository(BaseAlchemyRepository):
    def get_by_user_id(self, user_id: int) -> UserPerson | None:
        """
        Get person assignment of the user

        Args:
            user_id: User ID

        Returns:
            UserPerson entity if found, else None
        """

        user_person_model = (
            self.db
                .query(UserPersonModel)
                .filter(UserPersonModel.user_id == user_id)
                .first()
        )

        if user_person_model is None:
            return None

        return self._to_entity(user_person_model)

    def save(self, user_person: UserPerson) -> UserPerson:
        """
        Save new person assignment; a stored assignment cannot be changed, so an
        existing one is returned unchanged

        Args:
            user_person: UserPerson entity to save

        Returns:
            Saved user person entity
        """

        if user_person.id is None:
            return self._insert(user_person)

        return user_person

    def _insert(self, user_person: UserPerson) -> UserPerson:
        user_person_model = UserPersonModel(
            user_id=user_person.user_id,
            person_id=user_person.person_id,
        )
        self.db.add(user_person_model)
        self.db.flush()
        self.db.refresh(user_person_model)

        return self._to_entity(user_person_model)

    @staticmethod
    def _to_entity(user_person_model: UserPersonModel) -> UserPerson:
        return UserPerson(
            id=user_person_model.id,
            user_id=user_person_model.user_id,
            person_id=user_person_model.person_id,
        )
