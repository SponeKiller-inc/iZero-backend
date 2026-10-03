from typing import Self


class Address:
    """
    Represents an address.

    Attributes:
        id: The address ID.
        external_id: The external (e.g. RÚIAN) address identifier.
        street: The street name, if any.
        building_number: The building number (e.g. "číslo popisné/evidenční").
        orientation_number: The orientation number, if any.
        orientation_number_letter: The letter suffix of the orientation
            number, if any.
        district: The district / municipal part.
        city: The city name.
        postal_code: The postal code.
        country_id: The ID of the country this address belongs to.
    """

    def __init__(
        self,
        id: int | None,
        external_id: int,
        building_number: str,
        district: str,
        city: str,
        postal_code: int,
        country_id: int,
        street: str | None = None,
        orientation_number: str | None = None,
        orientation_number_letter: str | None = None,
    ):
        self.id = id
        self.external_id = external_id
        self.street = street
        self.building_number = building_number
        self.orientation_number = orientation_number
        self.orientation_number_letter = orientation_number_letter
        self.district = district
        self.city = city
        self.postal_code = postal_code
        self.country_id = country_id

    @classmethod
    def create(
        cls,
        external_id: int,
        building_number: str,
        district: str,
        city: str,
        postal_code: int,
        country_id: int,
        street: str | None = None,
        orientation_number: str | None = None,
        orientation_number_letter: str | None = None,
    ) -> Self:
        """
        Creates a new address.

        Args:
            external_id: The external (e.g. RÚIAN) address identifier.
            building_number: The building number.
            district: The district / municipal part.
            city: The city name.
            postal_code: The postal code.
            country_id: The ID of the country this address belongs to.
            street: The street name, if any.
            orientation_number: The orientation number, if any.
            orientation_number_letter: The letter suffix of the orientation
                number, if any.

        Returns:
            The newly created address.

        Raises:
            ValueError: If building_number, district or city is empty/blank,
                or postal_code is not a valid 5-digit value.
        """
        if not building_number or not building_number.strip():
            raise ValueError("Address's building number must be a non-empty string.")
        if not district or not district.strip():
            raise ValueError("Address's district must be a non-empty string.")
        if not city or not city.strip():
            raise ValueError("Address's city must be a non-empty string.")
        if not 0 <= postal_code <= 99999:
            raise ValueError("Address's postal code must be a 5-digit number.")

        return cls(
            external_id=external_id,
            building_number=building_number,
            district=district,
            city=city,
            postal_code=postal_code,
            country_id=country_id,
            street=street,
            orientation_number=orientation_number,
            orientation_number_letter=orientation_number_letter,
        )
