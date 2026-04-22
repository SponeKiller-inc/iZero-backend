from typing import Annotated

from app.domain.value_objects.identification import (
    RegistrationNumber, 
    BusinessTaxNumber, 
    ProprietorTaxNumber
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