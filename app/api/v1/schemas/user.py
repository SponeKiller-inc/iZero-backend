from typing import Dict, List
from datetime import datetime

from pydantic import BaseModel

class UserModuleOut(BaseModel):
    user_modules: Dict[str, List[str]]

class UserModuleIn(BaseModel):
    module_id: int
    valid_from: datetime
    valid_to: datetime
    