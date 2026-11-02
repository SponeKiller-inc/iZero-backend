from fastapi import Depends
from sqlalchemy.orm import Session

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


def get_retrieve_phone(db: Session = Depends(get_db)) -> RetrievePhone:
    return RetrievePhone(
        AlchemyPhonePrefixRepository(db),
        AlchemyPhoneRepository(db),
    )


def get_retrieve_email(db: Session = Depends(get_db)) -> RetrieveEmail:
    return RetrieveEmail(AlchemyEmailRepository(db))


def get_retrieve_person_addresses(
    db: Session = Depends(get_db),
) -> RetrievePersonAddresses:
    return RetrievePersonAddresses(
        AlchemyPersonRepository(db),
        AlchemyPersonAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        RetrieveAddress(AlchemyAddressRepository(db)),
    )


def get_assign_person_address(
    db: Session = Depends(get_db),
    retrieve_person_addresses: RetrievePersonAddresses = Depends(
        get_retrieve_person_addresses
    ),
) -> AssignPersonAddress:
    return AssignPersonAddress(
        AlchemyPersonRepository(db),
        AlchemyPersonAddressRepository(db),
        AlchemyAddressRepository(db),
        AlchemyAddressTypeRepository(db),
        SystemTimeProvider(),
        retrieve_person_addresses,
    )


def get_retrieve_natural_person(
    db: Session = Depends(get_db),
    retrieve_person_addresses: RetrievePersonAddresses = Depends(
        get_retrieve_person_addresses
    ),
) -> RetrieveNaturalPerson:
    return RetrieveNaturalPerson(
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        AlchemyPhoneRepository(db),
        AlchemyPhonePrefixRepository(db),
        AlchemyEmailRepository(db),
        SystemTimeProvider(),
        retrieve_person_addresses,
    )


def get_retrieve_entrepreneur(
    db: Session = Depends(get_db),
    retrieve_person_addresses: RetrievePersonAddresses = Depends(
        get_retrieve_person_addresses
    ),
) -> RetrieveEntrepreneur:
    return RetrieveEntrepreneur(
        AlchemyEntrepreneurRepository(db),
        AlchemyPhoneRepository(db),
        AlchemyPhonePrefixRepository(db),
        AlchemyEmailRepository(db),
        retrieve_person_addresses,
    )


def get_retrieve_company(
    db: Session = Depends(get_db),
    retrieve_natural_person: RetrieveNaturalPerson = Depends(
        get_retrieve_natural_person
    ),
    retrieve_person_addresses: RetrievePersonAddresses = Depends(
        get_retrieve_person_addresses
    ),
) -> RetrieveCompany:
    return RetrieveCompany(
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        AlchemyPhoneRepository(db),
        AlchemyPhonePrefixRepository(db),
        AlchemyEmailRepository(db),
        retrieve_natural_person,
        retrieve_person_addresses,
    )


def get_retrieve_person(
    db: Session = Depends(get_db),
    retrieve_natural_person: RetrieveNaturalPerson = Depends(
        get_retrieve_natural_person
    ),
    retrieve_entrepreneur: RetrieveEntrepreneur = Depends(
        get_retrieve_entrepreneur
    ),
    retrieve_company: RetrieveCompany = Depends(get_retrieve_company),
) -> RetrievePerson:
    return RetrievePerson(
        AlchemyPersonRepository(db),
        retrieve_natural_person,
        retrieve_entrepreneur,
        retrieve_company,
    )


def get_retrieve_user_person(
    db: Session = Depends(get_db),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
) -> RetrieveUserPerson:
    return RetrieveUserPerson(
        AlchemyUserPersonRepository(db),
        retrieve_person,
    )


def get_add_natural_person(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> AddNaturalPerson:
    return AddNaturalPerson(
        AlchemyPersonRepository(db),
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        SystemTimeProvider(),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )


def get_add_entrepreneur(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> AddEntrepreneur:
    return AddEntrepreneur(
        AlchemyPersonRepository(db),
        AlchemyEntrepreneurRepository(db),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )


def get_add_company(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    add_natural_person: AddNaturalPerson = Depends(get_add_natural_person),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> AddCompany:
    return AddCompany(
        AlchemyPersonRepository(db),
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        retrieve_phone,
        retrieve_email,
        add_natural_person,
        retrieve_person,
        assign_person_address,
    )


def get_add_user_person(
    db: Session = Depends(get_db),
    add_natural_person: AddNaturalPerson = Depends(get_add_natural_person),
    add_entrepreneur: AddEntrepreneur = Depends(get_add_entrepreneur),
    add_company: AddCompany = Depends(get_add_company),
) -> AddUserPerson:
    return AddUserPerson(
        AlchemyUserPersonRepository(db),
        add_natural_person,
        add_entrepreneur,
        add_company,
    )


def get_change_natural_person(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> ChangeNaturalPerson:
    return ChangeNaturalPerson(
        AlchemyPersonRepository(db),
        AlchemyNaturalPersonRepository(db),
        AlchemyTitleRepository(db),
        AlchemyPersonTitleRepository(db),
        SystemTimeProvider(),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )


def get_change_entrepreneur(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> ChangeEntrepreneur:
    return ChangeEntrepreneur(
        AlchemyPersonRepository(db),
        AlchemyEntrepreneurRepository(db),
        retrieve_phone,
        retrieve_email,
        retrieve_person,
        assign_person_address,
    )


def get_change_company(
    db: Session = Depends(get_db),
    retrieve_phone: RetrievePhone = Depends(get_retrieve_phone),
    retrieve_email: RetrieveEmail = Depends(get_retrieve_email),
    change_natural_person: ChangeNaturalPerson = Depends(
        get_change_natural_person
    ),
    retrieve_person: RetrievePerson = Depends(get_retrieve_person),
    assign_person_address: AssignPersonAddress = Depends(
        get_assign_person_address
    ),
) -> ChangeCompany:
    return ChangeCompany(
        AlchemyPersonRepository(db),
        AlchemyCompanyRepository(db),
        AlchemyLegalFormRepository(db),
        retrieve_phone,
        retrieve_email,
        change_natural_person,
        retrieve_person,
        assign_person_address,
    )


def get_change_user_person(
    db: Session = Depends(get_db),
    change_natural_person: ChangeNaturalPerson = Depends(
        get_change_natural_person
    ),
    change_entrepreneur: ChangeEntrepreneur = Depends(get_change_entrepreneur),
    change_company: ChangeCompany = Depends(get_change_company),
) -> ChangeUserPerson:
    return ChangeUserPerson(
        AlchemyUserPersonRepository(db),
        change_natural_person,
        change_entrepreneur,
        change_company,
    )
