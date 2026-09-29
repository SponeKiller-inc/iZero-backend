from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.dto.module.create_module_group import CreateModuleGroupIn
from app.application.use_cases.modules.create_module_group import CreateModuleGroup
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.module.module_group import (
    ModuleGroupSchemaIn,
    ModuleGroupSchemaOut,
)
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.module.module_group import (
    AlchemyModuleGroupRepository,
)
from app.infrastructure.services.time_provider import SystemTimeProvider

router = APIRouter(tags=["module-group"])


@router.post(
    "/groups",
    response_model=ResponseContainer[ModuleGroupSchemaOut],
    status_code=status.HTTP_201_CREATED,
)
async def create_module_group(
    module_group: ModuleGroupSchemaIn,
    db: Session = Depends(get_db),
):
    module_group_repository = AlchemyModuleGroupRepository(db)
    time_provider = SystemTimeProvider()

    module_group_creator = CreateModuleGroup(module_group_repository, time_provider)

    result = module_group_creator.execute(
        CreateModuleGroupIn(
            name=module_group.name,
            valid_from=module_group.valid_from,
        )
    )

    return ResponseContainer(data=ModuleGroupSchemaOut.model_validate(result))
