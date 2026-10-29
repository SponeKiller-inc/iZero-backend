from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.use_cases.banks.retrieve_banks import RetrieveBanks
from app.infrastructure.api.schemas.bank.bank_account import BankSchemaOut
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.bank.bank import AlchemyBankRepository

router = APIRouter(tags=["bank"])


@router.get(
    "/",
    response_model=ResponseContainer[list[BankSchemaOut]],
    status_code=status.HTTP_200_OK,
)
async def get_banks(db: Session = Depends(get_db)):
    bank_repository = AlchemyBankRepository(db)
    retrieve_banks = RetrieveBanks(bank_repository)

    banks = retrieve_banks.execute()

    return ResponseContainer(
        data=[BankSchemaOut.model_validate(bank) for bank in banks]
    )
