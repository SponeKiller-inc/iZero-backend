import re
from datetime import date
from typing import Any

import requests

from app.application.dto.address.address_provider import AddressProviderOut
from app.application.exceptions.address import AddressProviderError
from app.domain.shared.value_objects.location import CountryIsoCode
from app.infrastructure.providers.http_retry import call_with_retries

# Matches the leading part of RÚIAN's "adresa" text before the house number,
# optionally followed by a "č.p."/"č.ev." (house/registration number) label,
# e.g. "Jáchymova 68/5", "Zbonín č.ev. 14" or "č.p. 94".
_NAME_PATTERN = re.compile(
    r"^(?P<name>.*?)(?:\s*č\.\s?(?:p|ev)\.?)?\s+\d+(?:/\d+[A-Za-z]?)?$",
    re.IGNORECASE,
)


class RUIANAddressProvider:
    """
    Fetches address data from the Czech RÚIAN register (ČÚZK) via its public
    ArcGIS "AdresniMisto" REST service, exposing the `AddressProvider` port.

    All RÚIAN addresses are located in the Czech Republic, so `country_code`
    is hard-coded to CZE instead of being read from the external data.
    """

    _OUT_FIELDS = "kod,cislodomovni,cisloorientacni,cisloorientacnipismeno,psc,adresa"
    # Exclude expired / flagged-as-incorrect address points.
    _BASE_WHERE = "platido IS NULL AND nespravny IS NULL"

    def __init__(
        self,
        query_url: str,
        page_size: int,
        request_timeout_seconds: int,
        max_retries: int = 3,
        retry_backoff_seconds: float = 2.0,
    ):
        """
        Initialize provider.

        Args:
            query_url: URL of the RÚIAN "AdresniMisto" ArcGIS REST query endpoint.
            page_size: Number of records requested per page.
            request_timeout_seconds: Timeout for a single page request.
            max_retries: Number of additional attempts for a page request
                after a transient failure (timeout, connection error, or a
                5xx/429 response), before giving up.
            retry_backoff_seconds: Base delay between retries; doubled after
                each failed attempt (exponential backoff).
        """
        self.query_url = query_url
        self.page_size = page_size
        self.request_timeout_seconds = request_timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds

    def get_all(self) -> list[AddressProviderOut]:
        """
        Retrieve all addresses currently valid in the RÚIAN register.

        Returns:
            AddressProviderOut: All addresses known to RÚIAN.

        Raises:
            AddressProviderError: If RÚIAN cannot be reached or returns an error.
        """
        return self._fetch_all(self._BASE_WHERE)

    def get_modified(self, since: date) -> list[AddressProviderOut]:
        """
        Retrieve addresses whose validity started on or after the given date,
        i.e. addresses that were newly created or changed since then (RÚIAN
        represents an attribute change as a new address point version with
        its own "začátek platnosti").

        Args:
            since: Only addresses modified on or after this date are returned.

        Returns:
            AddressProviderOut: Addresses modified on or after `since`.

        Raises:
            AddressProviderError: If RÚIAN cannot be reached or returns an error.
        """
        where = f"{self._BASE_WHERE} AND platiod >= DATE '{since.isoformat()}'"
        return self._fetch_all(where)

    def _fetch_all(self, where: str) -> list[AddressProviderOut]:
        """
        Retrieve all address features matching the given filter, paginating
        through the result set.

        Args:
            where: ArcGIS SQL `where` clause to filter the features.

        Returns:
            AddressProviderOut: All addresses matching `where`.

        Raises:
            AddressProviderError: If RÚIAN cannot be reached or returns an error.
        """
        addresses: list[AddressProviderOut] = []
        offset = 0

        while True:
            features = self._fetch_page(where, offset)
            if not features:
                break

            addresses.extend(
                self._to_dto(feature["attributes"]) for feature in features
            )

            if len(features) < self.page_size:
                break
            offset += self.page_size

        return addresses

    def _fetch_page(self, where: str, offset: int) -> list[dict[str, Any]]:
        """
        Fetch a single page of address features from RÚIAN, retrying
        transient failures (timeouts, connection errors, 5xx/429 responses)
        with exponential backoff.

        Args:
            where: ArcGIS SQL `where` clause to filter the features.
            offset: Number of records to skip (for pagination).

        Returns:
            Raw ArcGIS features for the requested page.

        Raises:
            AddressProviderError: If RÚIAN cannot be reached or returns an
                error after exhausting all retry attempts.
        """
        try:
            response = call_with_retries(
                lambda: requests.get(
                    self.query_url,
                    params={
                        "where": where,
                        "outFields": self._OUT_FIELDS,
                        "orderByFields": "objectid",
                        "resultOffset": offset,
                        "resultRecordCount": self.page_size,
                        "f": "json",
                    },
                    timeout=self.request_timeout_seconds,
                ),
                max_retries=self.max_retries,
                base_delay_seconds=self.retry_backoff_seconds,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as e:
            raise AddressProviderError("Failed to fetch addresses from RÚIAN") from e

        if "error" in payload:
            raise AddressProviderError(f"RÚIAN returned an error: {payload['error']}")

        return payload.get("features", [])

    def _to_dto(self, attrs: dict[str, Any]) -> AddressProviderOut:
        """
        Converts a single RÚIAN feature into an `AddressProviderOut`.

        RÚIAN's free-text "adresa" field is formatted either as
        "<ulice> <č.p./č.o.>, <část obce>, <psč> <obec>" when the address
        lies on a named street, or as "<část obce>[ č.p./č.ev.] <č.p.>,
        <psč> <obec>" otherwise (with "<část obce>" omitted entirely when
        it matches the municipality name).
        """
        parts = [part.strip() for part in attrs["adresa"].split(",")]
        postal_code = attrs["psc"]

        city_part = parts[-1]
        postal_code_str = str(postal_code)
        city = (
            city_part[len(postal_code_str):].strip()
            if city_part.startswith(postal_code_str)
            else city_part
        )

        match = _NAME_PATTERN.match(parts[0])
        name = match.group("name").strip() if match else parts[0]

        if len(parts) >= 3:
            street, district = name or None, parts[-2]
        else:
            street, district = None, name or city

        orientation_number = attrs.get("cisloorientacni")

        return AddressProviderOut(
            external_id=attrs["kod"],
            street=street,
            building_number=str(attrs["cislodomovni"]),
            orientation_number=(
                str(orientation_number) if orientation_number is not None else None
            ),
            orientation_number_letter=attrs.get("cisloorientacnipismeno"),
            district=district,
            city=city,
            postal_code=postal_code,
            country_code=CountryIsoCode("CZE"),
        )
