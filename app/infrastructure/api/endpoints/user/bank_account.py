from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.dto.bank.bank_account import BankAccountIn
from app.application.dto.user.user_bank_account import UserBankAccountIn
from app.application.exceptions.bank import (
    BankAccountAlreadyExistsError,
    BankAccountNotFoundError,
    BankAccountValidationError,
    BankNotFoundError,
)
from app.application.use_cases.banks.add_bank_account import AddBankAccount
from app.application.use_cases.banks.change_bank_account import ChangeBankAccount
from app.application.use_cases.banks.retrieve_bank_account import RetrieveBankAccount
from app.application.use_cases.users.add_user_bank_account import AddUserBankAccount
from app.application.use_cases.users.change_user_bank_account import (
    ChangeUserBankAccount,
)
from app.application.use_cases.users.retrieve_user_bank_account import (
    RetrieveUserBankAccount,
)
from app.infrastructure.api.schemas.user.bank_account import (
    UserBankAccountSchemaIn,
    UserBankAccountSchemaOut,
)
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.bank.bank import AlchemyBankRepository
from app.infrastructure.repositories.bank.bank_account import (
    AlchemyBankAccountRepository,
)
from app.infrastructure.repositories.user.user_bank_account import (
    AlchemyUserBankAccountRepository,
)

router = APIRouter(tags=["user-bank-account"])


@router.get(
    "/{user_id}/bank-account",
    response_model=ResponseContainer[UserBankAccountSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_bank_account(user_id: int, db: Session = Depends(get_db)):
    bank_repository = AlchemyBankRepository(db)
    bank_account_repository = AlchemyBankAccountRepository(db)
    user_bank_account_repository = AlchemyUserBankAccountRepository(db)

    retrieve_bank_account = RetrieveBankAccount(
        bank_repository,
        bank_account_repository,
    )
    retrieve_user_bank_account = RetrieveUserBankAccount(
        user_bank_account_repository,
        retrieve_bank_account,
    )

    try:
        bank_account = retrieve_user_bank_account.execute(user_id)
    except BankAccountNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_ACCOUNT_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except BankNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ResponseContainer(data=bank_account)


@router.post(
    "/{user_id}/bank-account",
    response_model=ResponseContainer[UserBankAccountSchemaOut],
    status_code=status.HTTP_201_CREATED,
)
async def add_user_bank_account(
    user_id: int,
    bank_account: UserBankAccountSchemaIn,
    db: Session = Depends(get_db),
):
    # Initialize add user bank account
    bank_repository = AlchemyBankRepository(db)
    bank_account_repository = AlchemyBankAccountRepository(db)
    user_bank_account_repository = AlchemyUserBankAccountRepository(db)

    retrieve_bank_account = RetrieveBankAccount(
        bank_repository,
        bank_account_repository,
    )
    add_bank_account = AddBankAccount(
        bank_repository,
        bank_account_repository,
        retrieve_bank_account,
    )
    add_user_bank_account = AddUserBankAccount(
        user_bank_account_repository,
        add_bank_account,
    )

    dto = UserBankAccountIn(
        user_id=user_id,
        bank_account=BankAccountIn(
            bank_id=bank_account.bank_id,
            owner_name=bank_account.owner_name,
            account_prefix=bank_account.account_prefix,
            account_number=bank_account.account_number,
            iban=bank_account.iban,
        ),
    )

    try:
        added = add_user_bank_account.execute(dto)
    except BankAccountAlreadyExistsError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_ACCOUNT_ALREADY_EXISTS),
            status_code=status.HTTP_409_CONFLICT,
        )
    except BankNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except BankAccountValidationError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_ACCOUNT_VALIDATION_FAILED),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return ResponseContainer(data=added)


@router.put(
    "/{user_id}/bank-account",
    response_model=ResponseContainer[UserBankAccountSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def change_user_bank_account(
    user_id: int,
    bank_account: UserBankAccountSchemaIn,
    db: Session = Depends(get_db),
):
    # Initialize change user bank account
    bank_repository = AlchemyBankRepository(db)
    bank_account_repository = AlchemyBankAccountRepository(db)
    user_bank_account_repository = AlchemyUserBankAccountRepository(db)

    retrieve_bank_account = RetrieveBankAccount(
        bank_repository,
        bank_account_repository,
    )
    change_bank_account = ChangeBankAccount(
        bank_repository,
        bank_account_repository,
        retrieve_bank_account,
    )
    change_user_bank_account = ChangeUserBankAccount(
        user_bank_account_repository,
        change_bank_account,
    )

    dto = UserBankAccountIn(
        user_id=user_id,
        bank_account=BankAccountIn(
            bank_id=bank_account.bank_id,
            owner_name=bank_account.owner_name,
            account_prefix=bank_account.account_prefix,
            account_number=bank_account.account_number,
            iban=bank_account.iban,
        ),
    )

    # change user bank account
    try:
        changed = change_user_bank_account.execute(dto)
    except BankAccountNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_ACCOUNT_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except BankNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except BankAccountValidationError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.BANK_ACCOUNT_VALIDATION_FAILED),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return ResponseContainer(data=changed)
