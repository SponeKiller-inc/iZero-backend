from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.use_cases.modules.create_module import CreateModule
from app.application.dto.module.create_module import CreateModuleIn
from app.application.exceptions.module import ModuleGroupNotFoundError
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.module.module import AlchemyModuleRepository
from app.infrastructure.repositories.module.module_group import AlchemyModuleGroupRepository
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.module.module import ModuleIn, ModuleOut
from app.infrastructure.api.schemas.message_id import MessageId


router = APIRouter(tags=["module"])


@router.post(
    "",
    response_model=ResponseContainer[ModuleOut],
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    module: ModuleIn,
    db: Session = Depends(get_db),
):
    module_repository = AlchemyModuleRepository(db)
    module_group_repository = AlchemyModuleGroupRepository(db)
    time_provider = SystemTimeProvider()

    module_creator = CreateModule(
        module_repository,
        module_group_repository,
        time_provider,
    )

    try:
        result = module_creator.execute(
            CreateModuleIn(
                name=module.name,
                module_group_id=module.module_group_id,
                valid_from=module.valid_from,
            )
        )
    except ModuleGroupNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.MODULE_GROUP_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ResponseContainer(data=ModuleOut(
        id=result.id,
        name=result.name,
        module_group_id=result.module_group_id,
        valid_from=result.valid_from,
        valid_to=result.valid_to,
    ))

