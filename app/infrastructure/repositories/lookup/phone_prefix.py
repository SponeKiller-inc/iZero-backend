from app.domain.shared.entities.phone_prefix import PhonePrefix
from app.infrastructure.models.lookup.phone_prefixes import PhonePrefixModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyPhonePrefixRepository(BaseAlchemyRepository):
    def get(self, phone_prefix_id: int) -> PhonePrefix | None:
        """
        Get phone prefix by ID

        Args:
            phone_prefix_id: Phone prefix ID

        Returns:
            PhonePrefix entity if found, else None
        """

        model = (
            self.db
                .query(PhonePrefixModel)
                .filter(PhonePrefixModel.id == phone_prefix_id)
                .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_prefix(self, prefix: str) -> PhonePrefix | None:
        """
        Get phone prefix by its calling code

        Args:
            prefix: Calling code as digits only, without the leading "+" or "00"

        Returns:
            PhonePrefix entity if found, else None
        """

        model = (
            self.db
                .query(PhonePrefixModel)
                .filter(PhonePrefixModel.prefix == prefix)
                .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def save(self, phone_prefix: PhonePrefix) -> PhonePrefix:
        """
        Save new or existing phone prefix

        Args:
            phone_prefix: PhonePrefix entity to save

        Returns:
            Saved phone prefix entity
        """

        if phone_prefix.id is None:
            return self._insert(phone_prefix)
        else:
            return self._update(phone_prefix)

    def _insert(self, phone_prefix: PhonePrefix) -> PhonePrefix:
        model = PhonePrefixModel(prefix=phone_prefix.prefix, country_id=phone_prefix.country_id)
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, phone_prefix: PhonePrefix) -> PhonePrefix:
        model = (
            self.db
                .query(PhonePrefixModel)
                .filter(PhonePrefixModel.id == phone_prefix.id)
                .first()
        )

        model.prefix = phone_prefix.prefix
        model.country_id = phone_prefix.country_id

        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: PhonePrefixModel) -> PhonePrefix:
        return PhonePrefix(id=model.id, prefix=model.prefix, country_id=model.country_id)
