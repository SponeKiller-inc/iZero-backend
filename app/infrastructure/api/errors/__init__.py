from app.application.exceptions.base import ApplicationError
from app.infrastructure.api.errors.address.address import ADDRESS_ERRORS
from app.infrastructure.api.errors.module.module import MODULE_ERRORS
from app.infrastructure.api.errors.user.bank_account import BANK_ACCOUNT_ERRORS
from app.infrastructure.api.errors.user.person import PERSON_ERRORS
from app.infrastructure.api.errors.user.user import USER_ERRORS
from app.infrastructure.api.schemas.message_id import MessageId

# Response of each application error. Endpoints let these errors propagate, so
# that get_db rolls the request's transaction back before the response is built.
APPLICATION_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    **ADDRESS_ERRORS,
    **MODULE_ERRORS,
    **BANK_ACCOUNT_ERRORS,
    **PERSON_ERRORS,
    **USER_ERRORS,
}
