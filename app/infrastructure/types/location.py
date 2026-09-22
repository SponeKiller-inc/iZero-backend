from typing import Annotated

from sqlalchemy.orm import mapped_column

from app.domain.shared.value_objects.location import CountryIsoCode
from app.infrastructure.types.mapper import ValueObjectType

CountryIsoCodeType = Annotated[
    CountryIsoCode, 
    mapped_column(ValueObjectType(CountryIsoCode))
]