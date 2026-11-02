from fastapi import status

from app.application.exceptions.address import (
    AddressNotFoundError,
    AddressTypeNotFoundError,
)
from app.application.exceptions.base import ApplicationError
from app.infrastructure.api.schemas.message_id import MessageId

ADDRESS_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    AddressNotFoundError: (
        MessageId.ADDRESS_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
    AddressTypeNotFoundError: (
        MessageId.ADDRESS_TYPE_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
}
