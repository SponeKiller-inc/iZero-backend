from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.module import ModuleRepository
from app.domain.entity.module import ModuleService

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
 