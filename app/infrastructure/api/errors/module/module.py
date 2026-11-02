from fastapi import status

from app.application.exceptions.base import ApplicationError
from app.application.exceptions.module import ModuleGroupNotFoundError
from app.infrastructure.api.schemas.message_id import MessageId

MODULE_ERRORS: dict[type[ApplicationError], tuple[MessageId, int]] = {
    ModuleGroupNotFoundError: (
        MessageId.MODULE_GROUP_NOT_FOUND,
        status.HTTP_404_NOT_FOUND,
    ),
}
