from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.use_cases.lookup.retrieve_titles import RetrieveTitles
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.lookup.title import TitleSchemaOut
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.lookup.title import AlchemyTitleRepository

router = APIRouter(tags=["title"])


@router.get(
    "/titles",
    response_model=ResponseContainer[list[TitleSchemaOut]],
    status_code=status.HTTP_200_OK,
)
async def get_titles(db: Session = Depends(get_db)):
    title_repository = AlchemyTitleRepository(db)
    retrieve_titles = RetrieveTitles(title_repository)

    titles = retrieve_titles.execute()

    return ResponseContainer(
        data=[TitleSchemaOut.model_validate(title) for title in titles]
    )
