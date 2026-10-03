from app.domain.addresses.entities.country import Country
from app.domain.shared.value_objects.location import CountryIsoCode
from app.infrastructure.models.address.countries import CountryModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyCountryRepository(BaseAlchemyRepository):
    def get(self, country_id: int) -> Country | None:
        """
        Get a country by its ID

        Args:
            country_id (int): country id

        Returns:
            Country or None: country entity or None if no country found
        """

        model = (
            self.db.query(CountryModel)
            .filter(CountryModel.id == country_id)
            .first()
        )
        if not model:
            return None
        return self._to_entity(model)

    def get_by_code(self, code: str) -> Country | None:
        """
        Get a country by its ISO code

        Args:
            code (str): ISO 3166-1 alpha-3 country code

        Returns:
            Country or None: country entity or None if no country found
        """

        model = (
            self.db.query(CountryModel)
            .filter(CountryModel.code == code)
            .first()
        )
        if not model:
            return None
        return self._to_entity(model)

    def get_all(self) -> list[Country]:
        """
        Get all countries

        Returns:
            List of Country entities
        """

        models = self.db.query(CountryModel).all()
        return [self._to_entity(model) for model in models]

    def save(self, country: Country) -> Country:
        """
        Create or update Country.

        Args:
            country (Country): data to create or update country

        Returns:
            Country: newly created or updated country
        """
        if country.id is None:
            return self._insert(country)
        return self._update(country)

    def _insert(self, country: Country) -> Country:
        """
        Create Country.

        Args:
            country (Country): data to create country

        Returns:
            Country: newly created country
        """

        model = CountryModel(code=country.code.value, name=country.name)
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    def _update(self, country: Country) -> Country:
        """
        Update Country.

        Args:
            country (Country): data to update country

        Returns:
            Country: updated country
        """

        model = (
            self.db.query(CountryModel).filter(CountryModel.id == country.id).first()
        )

        model.code = country.code.value
        model.name = country.name
        self.db.flush()
        self.db.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: CountryModel) -> Country:
        return Country(
            id=model.id, code=CountryIsoCode(model.code), name=model.name
        )
