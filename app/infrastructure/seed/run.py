"""Entrypoint for seeding default configuration data, run right after `alembic upgrade head`."""
from sqlalchemy import func, select

from app.application.use_cases.seed.seed_czech_addresses import SeedCzechAddresses
from app.application.use_cases.seed.seed_default_address_types import (
    SeedDefaultAddressTypes,
)
from app.application.use_cases.seed.seed_default_admin import SeedDefaultAdmin
from app.application.use_cases.seed.seed_default_countries import (
    SeedDefaultCountries,
)
from app.application.use_cases.seed.seed_default_role_permissions import (
    SeedDefaultRolePermissions,
)
from app.application.use_cases.seed.seed_default_roles import SeedDefaultRoles
from app.application.use_cases.seed.seed_default_titles import SeedDefaultTitles
from app.infrastructure.config import settings
from app.infrastructure.database.session import db_session
from app.infrastructure.providers.ruian_address import RUIANAddressProvider
from app.infrastructure.repositories.address.address import AlchemyAddressRepository
from app.infrastructure.repositories.address.address_type import (
    AlchemyAddressTypeRepository,
)
from app.infrastructure.repositories.address.country import AlchemyCountryRepository
from app.infrastructure.repositories.auth.role_permission import (
    AlchemyRolePermissionRepository,
)
from app.infrastructure.repositories.lookup.role import AlchemyRoleRepository
from app.infrastructure.repositories.lookup.title import AlchemyTitleRepository
from app.infrastructure.repositories.user.user import AlchemyUserRepository
from app.infrastructure.repositories.user.user_role import AlchemyUserRoleRepository
from app.infrastructure.services.passlib_password_hasher import PasslibPasswordHasher
from app.infrastructure.services.time_provider import SystemTimeProvider

# Arbitrary fixed key for the advisory lock guarding this seed script.
SEED_LOCK_KEY = 837_412_901


def run() -> None:
    with db_session() as db:
        # Serialize concurrent replicas: without this, two replicas can both
        # observe a missing fixed-ID row and race on insert, crashing one of them.
        # Transaction-scoped lock auto-releases on commit/rollback (db_session's exit).
        db.execute(select(func.pg_advisory_xact_lock(SEED_LOCK_KEY)))

        # order matters: role_permission rows have a FK to roles
        SeedDefaultRoles(AlchemyRoleRepository(db)).execute()
        SeedDefaultTitles(AlchemyTitleRepository(db)).execute()
        SeedDefaultCountries(AlchemyCountryRepository(db)).execute()
        SeedDefaultAddressTypes(AlchemyAddressTypeRepository(db)).execute()
        SeedDefaultRolePermissions(
            AlchemyRolePermissionRepository(db),
            SystemTimeProvider(),
        ).execute()
        SeedDefaultAdmin(
            AlchemyUserRepository(db),
            AlchemyUserRoleRepository(db),
            PasslibPasswordHasher(),
            SystemTimeProvider(),
        ).execute()
        SeedCzechAddresses(
            RUIANAddressProvider(
                query_url=settings.ruian_query_url,
                page_size=settings.ruian_page_size,
                request_timeout_seconds=settings.ruian_request_timeout_seconds,
            ),
            AlchemyAddressRepository(db),
            AlchemyCountryRepository(db),
        ).execute()


if __name__ == "__main__":
    run()

