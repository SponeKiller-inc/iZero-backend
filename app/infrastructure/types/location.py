from typing import Annotated

from app.domain.value_objects.location import CountryIsoCode
from app.infrastructure.types.mapper import ValueObjectType

CountryIsoCode = Annotated[
    CountryIsoCode, 
    ValueObjectType(CountryIsoCode)
]