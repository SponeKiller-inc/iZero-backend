from __future__ import annotations

from dataclasses import dataclass

from app.domain.shared.value_objects.location import CountryIsoCode


@dataclass(frozen=True)
class AddressProviderOut:
    """DTO carrying address data as returned by an external address provider
    (e.g. RÚIAN), before it has been persisted and assigned an internal ID.
    """
    external_id: int
    street: str | None
    building_number: str
    orientation_number: str | None
    orientation_number_letter: str | None
    district: str
    city: str
    postal_code: int
    country_code: CountryIsoCode
