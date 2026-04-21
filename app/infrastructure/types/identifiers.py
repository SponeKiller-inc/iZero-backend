from typing import Annotated
from sqlalchemy.orm import mapped_column

from app.domain.value_objects.identifiers import RegistrationNumber, BusinessTaxNumber, ProprietorTaxNumber
from app.infrastructure.types.mapper import ValueObjectType

RegistrationNumber = Annotated[RegistrationNumber, mapped_column(ValueObjectType(RegistrationNumber), nullable=False)]
BusinessTaxNumber = Annotated[BusinessTaxNumber, mapped_column(ValueObjectType(BusinessTaxNumber), nullable=False)]
ProprietorTaxNumber = Annotated[ProprietorTaxNumber, mapped_column(ValueObjectType(ProprietorTaxNumber), nullable=False)]