from typing import Annotated

from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)
from app.infrastructure.types.mapper import ValueObjectType

RegistrationNumber = Annotated[
    RegistrationNumber,
    ValueObjectType(RegistrationNumber)
]
VatNumber = Annotated[
    VatNumber,
    ValueObjectType(VatNumber)
]
