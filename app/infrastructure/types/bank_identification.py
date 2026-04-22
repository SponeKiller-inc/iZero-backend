from typing import Annotated

from app.domain.value_objects.bank_identification import (
    BankCode,
    AccountPrefix,
    AccountNumber,
    Swift,
    Iban,
)
from app.infrastructure.types.mapper import ValueObjectType

BankCode = Annotated[
    BankCode, 
    ValueObjectType(BankCode)
]

AccountPrefix = Annotated[
    AccountPrefix, 
    ValueObjectType(AccountPrefix)
]

AccountNumber = Annotated[
    AccountNumber, 
    ValueObjectType(AccountNumber)
]

Swift = Annotated[
    Swift, 
    ValueObjectType(Swift)
]

Iban = Annotated[
    Iban, 
    ValueObjectType(Iban)
]