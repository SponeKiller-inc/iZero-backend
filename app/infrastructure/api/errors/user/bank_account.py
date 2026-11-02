from fastapi import status

from app.application.exceptions.bank import (
    BankAccountAlreadyExistsError,
    BankAccountNotFoundError,
    BankAccountValidationError,
    BankNotFoundError,
)
from app.application.exceptions.base import ApplicationError
from app.infrastructure.api.schemas.message_id import MessageId

BANK_ACCOUNT_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    BankAccountAlreadyExistsError: (
        MessageId.BANK_ACCOUNT_ALREADY_EXISTS,
        status.HTTP_409_CONFLICT,
    ),
    BankAccountNotFoundError: (
        MessageId.BANK_ACCOUNT_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
    BankAccountValidationError: (
        MessageId.BANK_ACCOUNT_VALIDATION_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    BankNotFoundError: (
        MessageId.BANK_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
}
