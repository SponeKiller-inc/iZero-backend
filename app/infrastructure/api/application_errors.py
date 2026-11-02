from fastapi import status

from app.application.exceptions.address import (
    AddressNotFoundError,
    AddressTypeNotFoundError,
)
from app.application.exceptions.auth import IdentityProviderError
from app.application.exceptions.bank import (
    BankAccountAlreadyExistsError,
    BankAccountNotFoundError,
    BankAccountValidationError,
    BankNotFoundError,
)
from app.application.exceptions.base import ApplicationError
from app.application.exceptions.contact import (
    EmailValidationError,
    PhoneValidationError,
)
from app.application.exceptions.module import ModuleGroupNotFoundError
from app.application.exceptions.person import (
    PersonAlreadyExistsError,
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
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

# Response of each application error. Endpoints let these errors propagate, so
# that get_db rolls the request's transaction back before the response is built.
APPLICATION_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    AddressNotFoundError: (
        MessageId.ADDRESS_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
    AddressTypeNotFoundError: (
        MessageId.ADDRESS_TYPE_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
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
    EmailValidationError: (
        MessageId.EMAIL_VALIDATION_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    IdentityProviderError: (
        MessageId.AUTH_IDENTITY_PROVIDER_FAILED,
        status.HTTP_400_BAD_REQUEST,
    ),
    InvalidCurrentPasswordError: (
        MessageId.USER_INVALID_CURRENT_PASSWORD,
        status.HTTP_400_BAD_REQUEST,
    ),
    ModuleGroupNotFoundError: (
        MessageId.MODULE_GROUP_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
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
