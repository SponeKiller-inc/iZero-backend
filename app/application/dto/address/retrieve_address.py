from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrieveAddressOut:
    """DTO carrying address data returned by the retrieve address use-cases."""
    id: int
    external_id: int
    street: str | None
    building_number: str
    orientation_number: str | None
    orientation_number_letter: str | None
    district: str | None
    city: str
    postal_code: int
    country_id: int
