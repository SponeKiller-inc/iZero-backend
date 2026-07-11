from enum import Enum

# 1. Number MainEntity
# 2. Number SubEntity
# 3. Last three are for count

class MessageId(int, Enum):
    USER_NOT_FOUND = 10001