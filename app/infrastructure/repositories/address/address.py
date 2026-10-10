from sqlalchemy.dialects.postgresql import insert

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

    def get_by_external_id(self, external_id: int, country_id: int) -> Address | None:
        """
        Get address by its external (e.g. RÚIAN) ID and country

        Args:
            external_id: External address ID
            country_id: ID of the country the address belongs to

        Returns:
            Address entity if found, else None
        """

        address_model = (
            self.db
                .query(AddressModel)
                .filter(
                    AddressModel.external_id == external_id,
                    AddressModel.country_id == country_id,
                )
                .first()
        )

        if address_model is None:
            return None

        return self._to_entity(address_model)

    def exists_for_country(self, country_id: int) -> bool:
        """
        Check whether any address already exists for the given country

        Args:
            country_id: Country ID

        Returns:
            True if at least one address exists for the country, else False
        """

        return (
            self.db
                .query(AddressModel.id)
                .filter(AddressModel.country_id == country_id)
                .first()
            is not None
        )

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

    def upsert_many(self, addresses: list[Address]) -> None:
        """
        Bulk insert addresses, overwriting existing ones matched by external
        ID and country, in a single statement. Existing rows keep their `id`.

        Args:
            addresses: Address entities to insert or update; their `id` is
                ignored. If the same external ID and country appear more
                than once, the last occurrence wins.
        """

        unique = {(a.external_id, a.country_id): a for a in addresses}
        if not unique:
            return

        stmt = insert(AddressModel)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_addresses_external_id_country_id",
            set_={
                "street": stmt.excluded.street,
                "building_number": stmt.excluded.building_number,
                "orientation_number": stmt.excluded.orientation_number,
                "orientation_number_letter": stmt.excluded.orientation_number_letter,
                "district": stmt.excluded.district,
                "city": stmt.excluded.city,
                "postal_code": stmt.excluded.postal_code,
                "updated_at": stmt.excluded.updated_at,
            },
        )

        self.db.execute(
            stmt,
            [
                {
                    "external_id": address.external_id,
                    "street": address.street,
                    "building_number": address.building_number,
                    "orientation_number": address.orientation_number,
                    "orientation_number_letter": address.orientation_number_letter,
                    "district": address.district,
                    "city": address.city,
                    "postal_code": address.postal_code,
                    "country_id": address.country_id,
                }
                for address in unique.values()
            ],
        )

    def _insert(self, address: Address) -> Address:
        address_model = AddressModel(
            external_id=address.external_id,
            street=address.street,
            building_number=address.building_number,
            orientation_number=address.orientation_number,
            orientation_number_letter=address.orientation_number_letter,
            district=address.district,
            city=address.city,
            postal_code=address.postal_code,
            country_id=address.country_id,
        )
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

        address_model.external_id = address.external_id
        address_model.street = address.street
        address_model.building_number = address.building_number
        address_model.orientation_number = address.orientation_number
        address_model.orientation_number_letter = address.orientation_number_letter
        address_model.district = address.district
        address_model.city = address.city
        address_model.postal_code = address.postal_code
        address_model.country_id = address.country_id

        self.db.flush()
        self.db.refresh(address_model)

        return self._to_entity(address_model)

    @staticmethod
    def _to_entity(address_model: AddressModel) -> Address:
        return Address(
            id=address_model.id,
            external_id=address_model.external_id,
            street=address_model.street,
            building_number=address_model.building_number,
            orientation_number=address_model.orientation_number,
            orientation_number_letter=address_model.orientation_number_letter,
            district=address_model.district,
            city=address_model.city,
            postal_code=address_model.postal_code,
            country_id=address_model.country_id,
        )