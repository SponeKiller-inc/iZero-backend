from typing import Annotated

from app.domain.shared.value_objects.location import CountryIsoCode
from app.infrastructure.types.mapper import ValueObjectType

from sqlalchemy.orm import mapped_column

CountryIsoCodeType = Annotated[
    CountryIsoCode, 
    mapped_column(ValueObjectType(CountryIsoCode))
]