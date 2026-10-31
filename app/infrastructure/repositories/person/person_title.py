from datetime import datetime

from app.domain.persons.entities.person_title import PersonTitle
from app.infrastructure.models.person.person_titles import PersonTitleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyPersonTitleRepository(BaseAlchemyRepository):
    def get(self, person_id: int, ref_date: datetime) -> list[PersonTitle]:
        """
        Get title assignments of the person valid at the reference date

        Args:
            person_id: Person ID
            ref_date: Reference date

        Returns:
            List of PersonTitle entities, empty if the person holds no title
        """

        return [
            self._to_entity(person_title_model)
            for person_title_model in (
                self.db
                    .query(PersonTitleModel)
                    .filter(
                        PersonTitleModel.person_id == person_id,
                        PersonTitleModel.valid_at(ref_date),
                    )
                    .order_by(PersonTitleModel.id)
                    .all()
            )
        ]

    def save(self, person_title: PersonTitle) -> PersonTitle:
        """
        Save new or existing title assignment

        Args:
            person_title: PersonTitle entity to save

        Returns:
            Saved person title entity
        """

        if person_title.id is None:
            return self._insert(person_title)
        else:
            return self._update(person_title)

    def _insert(self, person_title: PersonTitle) -> PersonTitle:
        person_title_model = PersonTitleModel(
            person_id=person_title.person_id,
            title_id=person_title.title_id,
            validity=person_title.validity,
        )
        self.db.add(person_title_model)
        self.db.flush()
        self.db.refresh(person_title_model)

        return self._to_entity(person_title_model)

    def _update(self, person_title: PersonTitle) -> PersonTitle:
        person_title_model = (
            self.db
                .query(PersonTitleModel)
                .filter(PersonTitleModel.id == person_title.id)
                .first()
        )

        person_title_model.person_id = person_title.person_id
        person_title_model.title_id = person_title.title_id
        person_title_model.validity = person_title.validity

        self.db.flush()
        self.db.refresh(person_title_model)

        return self._to_entity(person_title_model)

    @staticmethod
    def _to_entity(person_title_model: PersonTitleModel) -> PersonTitle:
        return PersonTitle(
            id=person_title_model.id,
            person_id=person_title_model.person_id,
            title_id=person_title_model.title_id,
            validity=person_title_model.validity,
        )
