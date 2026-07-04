from sqlalchemy.orm import Session
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.users.retrieve_modules import RetrieveModules
from app.application.exceptions.user import UserModuleNotFoundError
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.module.module import AlchemyModuleRepository
from app.infrastructure.repositories.module_group.module_group import AlchemyModuleGroupRepository
from app.infrastructure.repositories.user.user_module import AlchemyUserModuleRepository
from app.infrastructure.services.time_provider import SystemTimeProvider


router = APIRouter(tags=["user-module"])


@router.get(
    "/{user_id}/modules", 
    response_model=Dict[str, List[str]], 
    status_code=status.HTTP_200_OK
)
async def get_user_modules(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Initialize retrieve modules
    user_module_repository = AlchemyUserModuleRepository(db)
    module_repository = AlchemyModuleRepository(db)
    module_group_repository = AlchemyModuleGroupRepository(db)
    time_provider = SystemTimeProvider()

    retrieve_modules = RetrieveModules(
        user_module_repository,
        module_repository,
        module_group_repository,
        time_provider,
    )

    try:
        return retrieve_modules.execute(user_id)
    except UserModuleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user modules found",
        )