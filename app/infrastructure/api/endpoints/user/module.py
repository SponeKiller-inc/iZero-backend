from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.application.use_cases.users.retrieve_modules import RetrieveModules
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.module.module import AlchemyModuleRepository
from app.infrastructure.repositories.module.module_group import AlchemyModuleGroupRepository
from app.infrastructure.repositories.user.user_module import AlchemyUserModuleRepository
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.user.module import RetrieveModulesOut
from app.infrastructure.api.schemas.message_id import MessageId


router = APIRouter(tags=["user-module"])


@router.get(
    "/{user_id}/modules", 
    response_model=ResponseContainer[List[RetrieveModulesOut]], 
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

    user_modules = retrieve_modules.execute(user_id)

    if not user_modules:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ResponseContainer(message_id=MessageId.USER_NOT_FOUND)
        )
    
    return user_modules