from fastapi import status

from app.application.exceptions.auth import IdentityProviderError
from app.application.exceptions.base import ApplicationError
from app.application.exceptions.user import (
    InvalidCurrentPasswordError,
    PasswordChangeNotSupportedError,
    PasswordConfirmationMismatchError,
    PasswordSameAsCurrentError,
    PasswordTooLongError,
    PasswordTooShortError,
    RegisterLocalError,
    RegisterOauthError,
    UserCannotBeDeletedError,
    UserDeleteForbiddenError,
    UserNotFoundError,
)
from app.infrastructure.api.schemas.message_id import MessageId

USER_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    IdentityProviderError: (
        MessageId.AUTH_IDENTITY_PROVIDER_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    InvalidCurrentPasswordError: (
        MessageId.USER_INVALID_CURRENT_PASSWORD,
        status.HTTP_400_BAD_REQUEST,
    ),
    PasswordChangeNotSupportedError: (
        MessageId.USER_PASSWORD_CHANGE_NOT_SUPPORTED,
        status.HTTP_409_CONFLICT,
    ),
    PasswordConfirmationMismatchError: (
        MessageId.USER_PASSWORD_CONFIRMATION_MISMATCH,
        status.HTTP_400_BAD_REQUEST,
    ),
    PasswordSameAsCurrentError: (
        MessageId.USER_PASSWORD_SAME_AS_CURRENT,
        status.HTTP_400_BAD_REQUEST,
    ),
    PasswordTooLongError: (
        MessageId.USER_PASSWORD_TOO_LONG,
        status.HTTP_400_BAD_REQUEST,
    ),
    PasswordTooShortError: (
        MessageId.USER_PASSWORD_TOO_SHORT,
        status.HTTP_400_BAD_REQUEST,
    ),
    RegisterLocalError: (
        MessageId.USER_ALREADY_EXISTS,
        status.HTTP_409_CONFLICT,
    ),
    RegisterOauthError: (
        MessageId.USER_ALREADY_EXISTS,
        status.HTTP_409_CONFLICT,
    ),
    UserCannotBeDeletedError: (
        MessageId.USER_CANNOT_BE_DELETED,
        status.HTTP_409_CONFLICT,
    ),
    UserDeleteForbiddenError: (
        MessageId.AUTH_NOT_AUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ),
    UserNotFoundError: (
        MessageId.USER_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
}
