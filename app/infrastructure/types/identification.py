from typing import Annotated

from app.domain.shared.value_objects.identification import (
    BusinessTaxNumber,
    ProprietorTaxNumber,
    RegistrationNumber,
)
from app.infrastructure.types.mapper import ValueObjectType

RegistrationNumber = Annotated[
    RegistrationNumber, 
    ValueObjectType(RegistrationNumber)
]
BusinessTaxNumber = Annotated[
    BusinessTaxNumber, 
    ValueObjectType(BusinessTaxNumber)
]
ProprietorTaxNumber = Annotated[
    ProprietorTaxNumber, 
    ValueObjectType(ProprietorTaxNumber)
]