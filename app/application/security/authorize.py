from functools import wraps

from app.application.security.auth_hash import AuthHash
from app.application.exceptions.auth import AuthHashVerificationError
from app.application.security.auth_context import AuthContext
from app.application.security.hash_context import HashContext
from app.application.security.secret_message_context import SecretMessageContext
from app.application.constants.security import SecurityConstants
from app.application.constants.use_case import UseCase
from app.domain.shared.constants.entity_type import EntityType

def authorize(entity: EntityType, use_case: UseCase):
    # entity/use_case must match what Authenticate.execute hashed at login time
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            caller_id = AuthContext.get()
            hash_val = HashContext.get()
            secret_message = SecretMessageContext.get()
            auth_hash = AuthHash(SecurityConstants.AUTH_SECRET)

            if not auth_hash.verify(hash_val, caller_id, secret_message, entity.value, use_case.value):
                raise AuthHashVerificationError("Auth hash verification failed")

            return func(*args, **kwargs)
        return wrapper
    return decorator