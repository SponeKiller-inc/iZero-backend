from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.use_cases.lookup.retrieve_phone_prefixes import (
    RetrievePhonePrefixes,
)
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.lookup.phone_prefix import PhonePrefixSchemaOut
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.lookup.phone_prefix import (
    AlchemyPhonePrefixRepository,
)

router = APIRouter(tags=["phone-prefix"])


@router.get(
    "/phone-prefixes",
    response_model=ResponseContainer[list[PhonePrefixSchemaOut]],
    status_code=status.HTTP_200_OK,
)
async def get_phone_prefixes(db: Session = Depends(get_db)):
    phone_prefix_repository = AlchemyPhonePrefixRepository(db)
    retrieve_phone_prefixes = RetrievePhonePrefixes(phone_prefix_repository)

    phone_prefixes = retrieve_phone_prefixes.execute()

    return ResponseContainer(
        data=[
            PhonePrefixSchemaOut.model_validate(phone_prefix)
            for phone_prefix in phone_prefixes
        ]
    )
