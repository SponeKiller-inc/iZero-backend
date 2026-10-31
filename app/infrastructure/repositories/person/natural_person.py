from app.domain.persons.entities.natural_person import NaturalPerson
from app.infrastructure.models.person.natural_persons import NaturalPersonModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyNaturalPersonRepository(BaseAlchemyRepository):
    def get_by_person_id(self, person_id: int) -> NaturalPerson | None:
        """
        Get natural person details by person ID

        Args:
            person_id: Person ID

        Returns:
            NaturalPerson entity if found, else None
        """

        natural_person_model = (
            self.db
                .query(NaturalPersonModel)
                .filter(NaturalPersonModel.person_id == person_id)
                .first()
        )

        if natural_person_model is None:
            return None

        return self._to_entity(natural_person_model)

    def save(self, natural_person: NaturalPerson) -> NaturalPerson:
        """
        Save new or existing natural person details

        Args:
            natural_person: NaturalPerson entity to save

        Returns:
            Saved natural person entity
        """

        if natural_person.id is None:
            return self._insert(natural_person)
        else:
            return self._update(natural_person)

    def _insert(self, natural_person: NaturalPerson) -> NaturalPerson:
        natural_person_model = NaturalPersonModel(
            person_id=natural_person.person_id,
            first_name=natural_person.first_name,
            last_name=natural_person.last_name,
            date_of_birth=natural_person.date_of_birth,
            phone_id=natural_person.phone_id,
            email_id=natural_person.email_id,
        )
        self.db.add(natural_person_model)
        self.db.flush()
        self.db.refresh(natural_person_model)

        return self._to_entity(natural_person_model)

    def _update(self, natural_person: NaturalPerson) -> NaturalPerson:
        natural_person_model = (
            self.db
                .query(NaturalPersonModel)
                .filter(NaturalPersonModel.id == natural_person.id)
                .first()
        )

        natural_person_model.first_name = natural_person.first_name
        natural_person_model.last_name = natural_person.last_name
        natural_person_model.date_of_birth = natural_person.date_of_birth
        natural_person_model.phone_id = natural_person.phone_id
        natural_person_model.email_id = natural_person.email_id

        self.db.flush()
        self.db.refresh(natural_person_model)

        return self._to_entity(natural_person_model)

    @staticmethod
    def _to_entity(natural_person_model: NaturalPersonModel) -> NaturalPerson:
        return NaturalPerson(
            id=natural_person_model.id,
            person_id=natural_person_model.person_id,
            first_name=natural_person_model.first_name,
            last_name=natural_person_model.last_name,
            date_of_birth=natural_person_model.date_of_birth,
            phone_id=natural_person_model.phone_id,
            email_id=natural_person_model.email_id,
        )
