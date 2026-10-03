from app.domain.addresses.entities.address_type import AddressType
from app.infrastructure.models.address.address_types import AddressTypeModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyAddressTypeRepository(BaseAlchemyRepository):
    def get_by_type(self, address_type: str) -> AddressType | None:
        """
        Get an address type by its natural-key type ("permanent" or "mailing").

        Args:
            address_type (str): address type's type

        Returns:
            AddressType or None: address type entity or None if no address
                type found
        """

        model = (
            self.db.query(AddressTypeModel)
            .filter(AddressTypeModel.type == address_type)
            .first()
        )
        if not model:
            return None
        return self._to_entity(model)

    def save(self, address_type: AddressType) -> AddressType:
        """
        Create or update AddressType.

        Args:
            address_type (AddressType): data to create or update address type

        Returns:
            AddressType: newly created or updated address type
        """

        if address_type.id is None:
            return self._insert(address_type)
        return self._update(address_type)

    def _insert(self, address_type: AddressType) -> AddressType:
        """
        Create AddressType. The id is DB-assigned (auto-increment).

        Args:
            address_type (AddressType): data to create address type

        Returns:
            AddressType: newly created address type
        """

        model = AddressTypeModel(
            type=address_type.type, description=address_type.description
        )
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, address_type: AddressType) -> AddressType:
        """
        Update AddressType.

        Args:
            address_type (AddressType): data to update address type

        Returns:
            AddressType: updated address type
        """

        model = (
            self.db.query(AddressTypeModel)
            .filter(AddressTypeModel.id == address_type.id)
            .first()
        )

        model.type = address_type.type
        model.description = address_type.description
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: AddressTypeModel) -> AddressType:
        return AddressType(
            id=model.id, type=model.type, description=model.description
        )
