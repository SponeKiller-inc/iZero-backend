from datetime import datetime

from app.domain.persons.entities.person_address import PersonAddress
from app.infrastructure.models.person.person_addresses import PersonAddressModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyPersonAddressRepository(BaseAlchemyRepository):
    def get(self, person_id: int, ref_date: datetime) -> list[PersonAddress]:
        """
        Get address assignments of the person valid at the reference date

        Args:
            person_id: Person ID
            ref_date: Reference date

        Returns:
            List of PersonAddress entities, empty if the person has no address
        """

        return [
            self._to_entity(person_address_model)
            for person_address_model in (
                self.db
                    .query(PersonAddressModel)
                    .filter(
                        PersonAddressModel.person_id == person_id,
                        PersonAddressModel.valid_at(ref_date),
                    )
                    .order_by(PersonAddressModel.id)
                    .all()
            )
        ]

    def save(self, person_address: PersonAddress) -> PersonAddress:
        """
        Save new or existing address assignment

        Args:
            person_address: PersonAddress entity to save

        Returns:
            Saved person address entity
        """

        if person_address.id is None:
            return self._insert(person_address)
        else:
            return self._update(person_address)

    def _insert(self, person_address: PersonAddress) -> PersonAddress:
        person_address_model = PersonAddressModel(
            person_id=person_address.person_id,
            address_id=person_address.address_id,
            address_type_id=person_address.address_type_id,
            validity=person_address.validity,
        )
        self.db.add(person_address_model)
        self.db.flush()
        self.db.refresh(person_address_model)

        return self._to_entity(person_address_model)

    def _update(self, person_address: PersonAddress) -> PersonAddress:
        person_address_model = (
            self.db
                .query(PersonAddressModel)
                .filter(PersonAddressModel.id == person_address.id)
                .first()
        )

        person_address_model.person_id = person_address.person_id
        person_address_model.address_id = person_address.address_id
        person_address_model.address_type_id = person_address.address_type_id
        person_address_model.validity = person_address.validity

        self.db.flush()
        self.db.refresh(person_address_model)

        return self._to_entity(person_address_model)

    @staticmethod
    def _to_entity(person_address_model: PersonAddressModel) -> PersonAddress:
        return PersonAddress(
            id=person_address_model.id,
            person_id=person_address_model.person_id,
            address_id=person_address_model.address_id,
            address_type_id=person_address_model.address_type_id,
            validity=person_address_model.validity,
        )
