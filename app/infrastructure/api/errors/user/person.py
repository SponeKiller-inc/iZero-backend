from fastapi import status

from app.application.exceptions.base import ApplicationError
from app.application.exceptions.contact import (
    EmailValidationError,
    PhoneValidationError,
)
from app.application.exceptions.person import (
    PersonAlreadyExistsError,
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
from app.infrastructure.api.schemas.message_id import MessageId

PERSON_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    EmailValidationError: (
        MessageId.EMAIL_VALIDATION_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    PersonAlreadyExistsError: (
        MessageId.PERSON_ALREADY_EXISTS,
        status.HTTP_409_CONFLICT,
    ),
    PersonNotFoundError: (
        MessageId.PERSON_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
    PersonTypeChangeNotAllowedError: (
        MessageId.PERSON_TYPE_CHANGE_NOT_ALLOWED,
        status.HTTP_409_CONFLICT,
    ),
    PersonValidationError: (
        MessageId.PERSON_VALIDATION_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    PhoneValidationError: (
        MessageId.PHONE_VALIDATION_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
}
