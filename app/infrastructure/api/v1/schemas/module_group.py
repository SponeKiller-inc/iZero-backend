from pydantic import BaseModel

class ModuleIn(BaseModel):
    name: str
    
class ModuleGroupIn(BaseModel):
    name: str