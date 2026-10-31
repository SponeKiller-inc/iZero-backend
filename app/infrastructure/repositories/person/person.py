from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person import Person
from app.infrastructure.models.person.persons import PersonModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyPersonRepository(BaseAlchemyRepository):
    def get(self, person_id: int) -> Person | None:
        """
        Get person by ID

        Args:
            person_id: Person ID

        Returns:
            Person entity if found, else None
        """

        person_model = (
            self.db
                .query(PersonModel)
                .filter(PersonModel.id == person_id)
                .first()
        )

        if person_model is None:
            return None

        return self._to_entity(person_model)

    def save(self, person: Person) -> Person:
        """
        Save new person; the person type cannot be changed (BR-8), so an existing
        person is returned unchanged

        Args:
            person: Person entity to save

        Returns:
            Saved person entity
        """

        if person.id is not None:
            return person

        person_model = PersonModel(person_type=person.person_type.value)
        self.db.add(person_model)
        self.db.flush()
        self.db.refresh(person_model)

        return self._to_entity(person_model)

    @staticmethod
    def _to_entity(person_model: PersonModel) -> Person:
        return Person(
            id=person_model.id,
            person_type=PersonType(person_model.person_type),
        )
