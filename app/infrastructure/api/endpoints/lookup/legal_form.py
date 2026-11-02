from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.use_cases.lookup.retrieve_legal_forms import (
    RetrieveLegalForms,
)
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.lookup.legal_form import LegalFormSchemaOut
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.lookup.legal_form import AlchemyLegalFormRepository

router = APIRouter(tags=["legal-form"])


@router.get(
    "/legal-forms",
    response_model=ResponseContainer[list[LegalFormSchemaOut]],
    status_code=status.HTTP_200_OK,
)
async def get_legal_forms(db: Session = Depends(get_db)):
    legal_form_repository = AlchemyLegalFormRepository(db)
    retrieve_legal_forms = RetrieveLegalForms(legal_form_repository)

    legal_forms = retrieve_legal_forms.execute()

    return ResponseContainer(
        data=[LegalFormSchemaOut.model_validate(legal_form) for legal_form in legal_forms]
    )
