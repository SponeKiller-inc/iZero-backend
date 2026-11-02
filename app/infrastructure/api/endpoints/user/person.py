from fastapi import APIRouter, Depends, status

from app.application.dto.person.company import CompanyIn
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person_address import AddressIn
from app.application.dto.user.user_person import UserPersonIn
from app.application.use_cases.users.add_user_person import AddUserPerson
from app.application.use_cases.users.change_user_person import ChangeUserPerson
from app.application.use_cases.users.retrieve_user_person import RetrieveUserPerson
from app.infrastructure.api.dependency.user.person import (
    get_add_user_person,
    get_change_user_person,
    get_retrieve_user_person,
)
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.schemas.person.company import CompanySchemaIn
from app.infrastructure.api.schemas.person.entrepreneur import EntrepreneurSchemaIn
from app.infrastructure.api.schemas.person.natural_person import NaturalPersonSchemaIn
from app.infrastructure.api.schemas.user.user_person import (
    UserPersonSchemaIn,
    UserPersonSchemaOut,
)

router = APIRouter(tags=["user-person"])


@router.get(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_person(
    user_id: int,
    retrieve_user_person: RetrieveUserPerson = Depends(
        get_retrieve_user_person
    ),
):
    person = retrieve_user_person.execute(user_id)

    return ResponseContainer(data=person)


@router.post(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_201_CREATED,
)
async def add_user_person(
    user_id: int,
    person: UserPersonSchemaIn,
    add_user_person: AddUserPerson = Depends(get_add_user_person),
):
    details = person.person
    addresses = [
        AddressIn(
            address_id=address.address_id,
            address_type_id=address.address_type_id,
        )
        for address in details.addresses
    ]

    match details:
        case NaturalPersonSchemaIn():
            person_dto = NaturalPersonIn(
                first_name=details.first_name,
                last_name=details.last_name,
                date_of_birth=details.date_of_birth,
                title_ids=details.title_ids,
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )
        case EntrepreneurSchemaIn():
            person_dto = EntrepreneurIn(
                name=details.name,
                registration_number=details.registration_number,
                vat_number=details.vat_number,
                is_vat_payer=details.is_vat_payer,
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )
        case CompanySchemaIn():
            representative = details.representative
            person_dto = CompanyIn(
                name=details.name,
                legal_form_id=details.legal_form_id,
                registration_number=details.registration_number,
                vat_number=details.vat_number,
                is_vat_payer=details.is_vat_payer,
                representative=NaturalPersonIn(
                    first_name=representative.first_name,
                    last_name=representative.last_name,
                    date_of_birth=representative.date_of_birth,
                    title_ids=representative.title_ids,
                    phone_prefix_id=representative.phone_prefix_id,
                    phone_number=representative.phone_number,
                    email=representative.email,
                    addresses=[
                        AddressIn(
                            address_id=address.address_id,
                            address_type_id=address.address_type_id,
                        )
                        for address in representative.addresses
                    ],
                ),
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )

    dto = UserPersonIn(user_id=user_id, person=person_dto)

    added = add_user_person.execute(dto)

    return ResponseContainer(data=added)


@router.put(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def change_user_person(
    user_id: int,
    person: UserPersonSchemaIn,
    change_user_person: ChangeUserPerson = Depends(get_change_user_person),
):
    details = person.person
    addresses = [
        AddressIn(
            address_id=address.address_id,
            address_type_id=address.address_type_id,
        )
        for address in details.addresses
    ]

    match details:
        case NaturalPersonSchemaIn():
            person_dto = NaturalPersonIn(
                first_name=details.first_name,
                last_name=details.last_name,
                date_of_birth=details.date_of_birth,
                title_ids=details.title_ids,
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )
        case EntrepreneurSchemaIn():
            person_dto = EntrepreneurIn(
                name=details.name,
                registration_number=details.registration_number,
                vat_number=details.vat_number,
                is_vat_payer=details.is_vat_payer,
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )
        case CompanySchemaIn():
            representative = details.representative
            person_dto = CompanyIn(
                name=details.name,
                legal_form_id=details.legal_form_id,
                registration_number=details.registration_number,
                vat_number=details.vat_number,
                is_vat_payer=details.is_vat_payer,
                representative=NaturalPersonIn(
                    first_name=representative.first_name,
                    last_name=representative.last_name,
                    date_of_birth=representative.date_of_birth,
                    title_ids=representative.title_ids,
                    phone_prefix_id=representative.phone_prefix_id,
                    phone_number=representative.phone_number,
                    email=representative.email,
                    addresses=[
                        AddressIn(
                            address_id=address.address_id,
                            address_type_id=address.address_type_id,
                        )
                        for address in representative.addresses
                    ],
                ),
                phone_prefix_id=details.phone_prefix_id,
                phone_number=details.phone_number,
                email=details.email,
                addresses=addresses,
            )

    dto = UserPersonIn(user_id=user_id, person=person_dto)

    changed = change_user_person.execute(dto)

    return ResponseContainer(data=changed)
