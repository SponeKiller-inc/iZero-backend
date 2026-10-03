from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.exceptions.address import AddressNotFoundError
from app.application.use_cases.addresses.retrieve_address import RetrieveAddress
from app.application.use_cases.addresses.retrieve_addresses import RetrieveAddresses
from app.infrastructure.api.schemas.address.address import AddressSchemaOut
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.address.address import AlchemyAddressRepository

router = APIRouter(tags=["address"])


@router.get(
    "/",
    response_model=ResponseContainer[list[AddressSchemaOut]],
    status_code=status.HTTP_200_OK,
)
async def get_addresses(db: Session = Depends(get_db)):
    address_repository = AlchemyAddressRepository(db)
    retrieve_addresses = RetrieveAddresses(address_repository)

    addresses = retrieve_addresses.execute()

    return ResponseContainer(
        data=[AddressSchemaOut.model_validate(address) for address in addresses]
    )


@router.get(
    "/{address_id}",
    response_model=ResponseContainer[AddressSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    address_repository = AlchemyAddressRepository(db)
    retrieve_address = RetrieveAddress(address_repository)

    try:
        address = retrieve_address.execute(address_id)
    except AddressNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.ADDRESS_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ResponseContainer(data=AddressSchemaOut.model_validate(address))
