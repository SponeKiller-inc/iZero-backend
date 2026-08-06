from enum import Enum

# 1. two numbers MainEntity
# 2. two numbers SubEntity
# 3. Last three are for count

class MessageId(int, Enum):
    USER_NOT_FOUND = 1000001
    AUTH_NOT_AUTHENTICATED = 2000001
    AUTH_NOT_AUTHORIZED = 2000002
    AUTH_NOT_ACCESS = 2000003
    SYSTEM_INTERNAL_FAIL = 9000001