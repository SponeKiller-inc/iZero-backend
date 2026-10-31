from enum import Enum
from typing import Self


class UseCase(str, Enum):
    USERS_ASSIGN_MODULE = "assign_module"
    USERS_RETRIEVE_MODULE = "retrieve_module"
    USERS_DELETE = "delete_user"
    USERS_CHANGE_PASSWORD = "change_password"
    AUTH_ASSIGN_ROLE_PERMISSION = "assign_role_permission"
    MODULES_CREATE = "create_module"
    MODULES_CREATE_GROUP = "create_module_group"
    BANKS_RETRIEVE = "retrieve_banks"
    BANKS_RETRIEVE_ACCOUNT = "retrieve_bank_account"
    BANKS_ADD_ACCOUNT = "add_bank_account"
    BANKS_CHANGE_ACCOUNT = "change_bank_account"
    BANKS_ADD_USER_ACCOUNT = "add_user_bank_account"
    BANKS_RETRIEVE_USER_ACCOUNT = "retrieve_user_bank_account"
    BANKS_CHANGE_USER_ACCOUNT = "change_user_bank_account"
    PERSONS_ADD = "add_person"
    PERSONS_RETRIEVE = "retrieve_person"
    PERSONS_CHANGE = "change_person"
    CONTACTS_RETRIEVE_PHONE = "retrieve_phone"
    CONTACTS_RETRIEVE_EMAIL = "retrieve_email"

    @classmethod
    def has_member(cls, name: str) -> bool:
        return name in cls.__members__

    @classmethod
    def get_member(cls, name: str) -> Self | None:
        return cls.__members__.get(name)