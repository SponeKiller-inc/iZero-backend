from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.dto.person.company import CompanyIn
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.natural_person import NaturalPersonIn
from app.application.dto.person.person_address import AddressIn
from app.application.dto.user.user_person import UserPersonIn
from app.application.exceptions.address import (
    AddressNotFoundError,
    AddressTypeNotFoundError,
)
from app.application.exceptions.contact import (
    EmailValidationError,
    PhoneValidationError,
)
from app.application.exceptions.person import (
    PersonAlreadyExistsError,
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
from app.application.use_cases.addresses.retrieve_address import RetrieveAddress
from app.application.use_cases.contacts.retrieve_email import RetrieveEmail
from app.application.use_cases.contacts.retrieve_phone import RetrievePhone
from app.application.use_cases.persons.add_company import AddCompany
from app.application.use_cases.persons.add_entrepreneur import AddEntrepreneur
from app.application.use_cases.persons.add_natural_person import AddNaturalPerson
from app.application.use_cases.persons.assign_person_address import AssignPersonAddress
from app.application.use_cases.persons.change_company import ChangeCompany
from app.application.use_cases.persons.change_entrepreneur import ChangeEntrepreneur
from app.application.use_cases.persons.change_natural_person import ChangeNaturalPerson
from app.application.use_cases.persons.retrieve_company import RetrieveCompany
from app.application.use_cases.persons.retrieve_entrepreneur import RetrieveEntrepreneur
from app.application.use_cases.persons.retrieve_natural_person import (
    RetrieveNaturalPerson,
)
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.application.use_cases.persons.retrieve_person_addresses import (
    RetrievePersonAddresses,
)
from app.application.use_cases.users.add_user_person import AddUserPerson
from app.application.use_cases.users.change_user_person import ChangeUserPerson
from app.application.use_cases.users.retrieve_user_person import RetrieveUserPerson
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.api.schemas.person.company import CompanySchemaIn
from app.infrastructure.api.schemas.person.entrepreneur import EntrepreneurSchemaIn
from app.infrastructure.api.schemas.person.natural_person import NaturalPersonSchemaIn
from app.infrastructure.api.schemas.user.user_person import (
    UserPersonSchemaIn,
    UserPersonSchemaOut,
)
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.address.address import AlchemyAddressRepository
from app.infrastructure.repositories.address.address_type import (
    AlchemyAddressTypeRepository,
)
from app.infrastructure.repositories.contact.email import AlchemyEmailRepository
from app.infrastructure.repositories.contact.phone import AlchemyPhoneRepository
from app.infrastructure.repositories.lookup.legal_form import AlchemyLegalFormRepository
from app.infrastructure.repositories.lookup.phone_prefix import (
    AlchemyPhonePrefixRepository,
)
from app.infrastructure.repositories.lookup.title import AlchemyTitleRepository
from app.infrastructure.repositories.person.company import AlchemyCompanyRepository
from app.infrastructure.repositories.person.entrepreneur import (
    AlchemyEntrepreneurRepository,
)
from app.infrastructure.repositories.person.natural_person import (
    AlchemyNaturalPersonRepository,
)
from app.infrastructure.repositories.person.person import AlchemyPersonRepository
from app.infrastructure.repositories.person.person_address import (
    AlchemyPersonAddressRepository,
)
from app.infrastructure.repositories.person.person_title import (
    AlchemyPersonTitleRepository,
)
from app.infrastructure.repositories.user.user_person import AlchemyUserPersonRepository
from app.infrastructure.services.time_provider import SystemTimeProvider

router = APIRouter(tags=["user-person"])


@router.get(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_person(user_id: int, db: Session = Depends(get_db)):
    # Initialize retrieve user person
    phone_repository = AlchemyPhoneRepository(db)
    phone_prefix_repository = AlchemyPhonePrefixRepository(db)
    email_repository = AlchemyEmailRepository(db)

    retrieve_person_addresses = RetrievePersonAddresses(
        AlchemyPersonRepository(db),
        AlchemyPersonAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        RetrieveAddress(AlchemyAddressRepository(db)),
    )
    retrieve_natural_person = RetrieveNaturalPerson(
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        SystemTimeProvider(),
        retrieve_person_addresses,
    )
    retrieve_entrepreneur = RetrieveEntrepreneur(
        AlchemyEntrepreneurRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_person_addresses,
    )
    retrieve_company = RetrieveCompany(
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_natural_person,
        retrieve_person_addresses,
    )
    retrieve_person = RetrievePerson(
        AlchemyPersonRepository(db),
        retrieve_natural_person,
        retrieve_entrepreneur,
        retrieve_company,
    )
    retrieve_user_person = RetrieveUserPerson(
        AlchemyUserPersonRepository(db),
        retrieve_person,
    )

    try:
        person = retrieve_user_person.execute(user_id)
    except PersonNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.PERSON_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ResponseContainer(data=person)


@router.post(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_201_CREATED,
)
async def add_user_person(
    user_id: int,
    person: UserPersonSchemaIn,
    db: Session = Depends(get_db),
):
    # Initialize add user person
    person_repository = AlchemyPersonRepository(db)
    phone_repository = AlchemyPhoneRepository(db)
    phone_prefix_repository = AlchemyPhonePrefixRepository(db)
    email_repository = AlchemyEmailRepository(db)

    retrieve_phone = RetrievePhone(phone_prefix_repository, phone_repository)
    retrieve_email = RetrieveEmail(email_repository)
    retrieve_person_addresses = RetrievePersonAddresses(
        person_repository,
        AlchemyPersonAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        RetrieveAddress(AlchemyAddressRepository(db)),
    )
    assign_person_address = AssignPersonAddress(
        person_repository,
        AlchemyPersonAddressRepository(db),
        AlchemyAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        retrieve_person_addresses,
    )
    retrieve_natural_person = RetrieveNaturalPerson(
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        SystemTimeProvider(),
        retrieve_person_addresses,
    )
    retrieve_entrepreneur = RetrieveEntrepreneur(
        AlchemyEntrepreneurRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_person_addresses,
    )
    retrieve_company = RetrieveCompany(
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_natural_person,
        retrieve_person_addresses,
    )
    retrieve_person = RetrievePerson(
        person_repository,
        retrieve_natural_person,
        retrieve_entrepreneur,
        retrieve_company,
    )

    add_natural_person = AddNaturalPerson(
        person_repository,
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        SystemTimeProvider(),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )
    add_entrepreneur = AddEntrepreneur(
        person_repository,
        AlchemyEntrepreneurRepository(db),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )
    add_company = AddCompany(
        person_repository,
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        retrieve_phone,
        retrieve_email,
        add_natural_person,
        retrieve_person,
        assign_person_address,
    )
    add_user_person = AddUserPerson(
        AlchemyUserPersonRepository(db),
        add_natural_person,
        add_entrepreneur,
        add_company,
    )

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

    # A caught error does not reach get_db, so what the use-case stored before
    # the failure has to be rolled back here, otherwise it would be committed
    try:
        added = add_user_person.execute(dto)
    except PersonAlreadyExistsError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PERSON_ALREADY_EXISTS,
            ),
            status_code=status.HTTP_409_CONFLICT,
        )
    except AddressNotFoundError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.ADDRESS_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except AddressTypeNotFoundError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.ADDRESS_TYPE_NOT_FOUND,
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except PersonValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PERSON_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except PhoneValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PHONE_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except EmailValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.EMAIL_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return ResponseContainer(data=added)


@router.put(
    "/{user_id}/person",
    response_model=ResponseContainer[UserPersonSchemaOut],
    status_code=status.HTTP_200_OK,
)
async def change_user_person(
    user_id: int,
    person: UserPersonSchemaIn,
    db: Session = Depends(get_db),
):
    # Initialize change user person
    person_repository = AlchemyPersonRepository(db)
    phone_repository = AlchemyPhoneRepository(db)
    phone_prefix_repository = AlchemyPhonePrefixRepository(db)
    email_repository = AlchemyEmailRepository(db)

    retrieve_phone = RetrievePhone(phone_prefix_repository, phone_repository)
    retrieve_email = RetrieveEmail(email_repository)
    retrieve_person_addresses = RetrievePersonAddresses(
        person_repository,
        AlchemyPersonAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        RetrieveAddress(AlchemyAddressRepository(db)),
    )
    assign_person_address = AssignPersonAddress(
        person_repository,
        AlchemyPersonAddressRepository(db),
        AlchemyAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        retrieve_person_addresses,
    )
    retrieve_natural_person = RetrieveNaturalPerson(
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        SystemTimeProvider(),
        retrieve_person_addresses,
    )
    retrieve_entrepreneur = RetrieveEntrepreneur(
        AlchemyEntrepreneurRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_person_addresses,
    )
    retrieve_company = RetrieveCompany(
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        phone_repository,
        phone_prefix_repository,
        email_repository,
        retrieve_natural_person,
        retrieve_person_addresses,
    )
    retrieve_person = RetrievePerson(
        person_repository,
        retrieve_natural_person,
        retrieve_entrepreneur,
        retrieve_company,
    )

    change_natural_person = ChangeNaturalPerson(
        person_repository,
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        SystemTimeProvider(),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )
    change_entrepreneur = ChangeEntrepreneur(
        person_repository,
        AlchemyEntrepreneurRepository(db),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )
    change_company = ChangeCompany(
        person_repository,
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        retrieve_phone,
        retrieve_email,
        change_natural_person,
        retrieve_person,
        assign_person_address,
    )
    change_user_person = ChangeUserPerson(
        AlchemyUserPersonRepository(db),
        change_natural_person,
        change_entrepreneur,
        change_company,
    )

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

    # A caught error does not reach get_db, so what the use-case stored before
    # the failure has to be rolled back here, otherwise it would be committed
    try:
        changed = change_user_person.execute(dto)
    except PersonNotFoundError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.PERSON_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except PersonTypeChangeNotAllowedError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PERSON_TYPE_CHANGE_NOT_ALLOWED,
            ),
            status_code=status.HTTP_409_CONFLICT,
        )
    except AddressNotFoundError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.ADDRESS_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except AddressTypeNotFoundError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.ADDRESS_TYPE_NOT_FOUND,
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except PersonValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PERSON_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except PhoneValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.PHONE_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except EmailValidationError:
        db.rollback()
        return JSONResponse(
            content=ResponseContainer(
                message_id=MessageId.EMAIL_VALIDATION_FAILED,
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return ResponseContainer(data=changed)
