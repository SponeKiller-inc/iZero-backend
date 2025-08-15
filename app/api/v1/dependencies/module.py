from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.module import ModuleRepository
from app.services.module import ModuleService

class ModuleDependencies(ModuleService):
    """
    Dependency container for module-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
    ):
        repo = ModuleRepository(session)
        super().__init__(repo)
 