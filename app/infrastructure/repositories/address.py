from app.domain.addresses.entities.address import Address
from app.infrastructure.models.address.addresses import AddressModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyAddressRepository(BaseAlchemyRepository):
    def get(self, address_id: int) -> Address | None:
        """
        Get address by ID

        Args:
            address_id: Address ID

        Returns:
            Address entity if found, else None
        """

        address_model = (
            self.db
                .query(AddressModel)
                .filter(AddressModel.id == address_id)
                .first()
        )

        if address_model is None:
            return None

        return self._to_entity(address_model)

    def get_all(self) -> list[Address]:
        """
        Get all addresses

        Returns:
            List of Address entities
        """

        return [
            self._to_entity(address_model)
            for address_model in self.db.query(AddressModel).all()
        ]

    def save(self, address: Address) -> Address:
        """
        Save new or existing address

        Args:
            address: Address entity to save

        Returns:
            Saved address entity
        """

        if address.id is None:
            return self._insert(address)
        else:
            return self._update(address)

    def _insert(self, address: Address) -> Address:
        address_model = AddressModel()
        self.db.add(address_model)
        self.db.flush()
        self.db.refresh(address_model)

        return self._to_entity(address_model)

    def _update(self, address: Address) -> Address:
        address_model = (
            self.db
                .query(AddressModel)
                .filter(AddressModel.id == address.id)
                .first()
        )

        self.db.flush()
        self.db.refresh(address_model)

        return self._to_entity(address_model)

    @staticmethod
    def _to_entity(address_model: AddressModel) -> Address:
        return Address(id=address_model.id)