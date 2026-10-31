from app.domain.shared.entities.phone import Phone
from app.domain.shared.value_objects.contact import PhoneNumber
from app.infrastructure.models.contact.phones import PhoneModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyPhoneRepository(BaseAlchemyRepository):
    def get(self, phone_id: int) -> Phone | None:
        """
        Get phone by ID

        Args:
            phone_id: Phone ID

        Returns:
            Phone entity if found, else None
        """

        phone_model = (
            self.db
                .query(PhoneModel)
                .filter(PhoneModel.id == phone_id)
                .first()
        )

        if phone_model is None:
            return None

        return self._to_entity(phone_model)

    def get_by_number(self, phone_prefix_id: int, number: str) -> Phone | None:
        """
        Get phone by its calling code and national number

        Args:
            phone_prefix_id: Phone prefix ID
            number: National phone number

        Returns:
            Phone entity if found, else None
        """

        phone_model = (
            self.db
                .query(PhoneModel)
                .filter(PhoneModel.phone_prefix_id == phone_prefix_id, PhoneModel.number == number)
                .first()
        )

        if phone_model is None:
            return None

        return self._to_entity(phone_model)

    def save(self, phone: Phone) -> Phone:
        """
        Save new phone; a stored phone is shared by every record using it and cannot
        be changed, so an existing one is returned unchanged

        Args:
            phone: Phone entity to save

        Returns:
            Saved phone entity
        """

        if phone.id is None:
            return self._insert(phone)

        return phone

    def _insert(self, phone: Phone) -> Phone:
        phone_model = PhoneModel(phone_prefix_id=phone.phone_prefix_id, number=phone.number.value)
        self.db.add(phone_model)
        self.db.flush()
        self.db.refresh(phone_model)

        return self._to_entity(phone_model)

    @staticmethod
    def _to_entity(phone_model: PhoneModel) -> Phone:
        return Phone(
            id=phone_model.id,
            phone_prefix_id=phone_model.phone_prefix_id,
            number=PhoneNumber(phone_model.number),
        )
