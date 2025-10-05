from datetime import datetime

from pydantic import BaseModel

class UserModuleIn(BaseModel):
    module_id: int
    valid_from: datetime
    valid_to: datetime
    