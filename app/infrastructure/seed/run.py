"""Entrypoint for seeding default configuration data, run right after `alembic upgrade head`."""
from app.infrastructure.database.session import db_session
from app.infrastructure.repositories.lookup.role import AlchemyRoleRepository
from app.infrastructure.repositories.lookup.title import AlchemyTitleRepository
from app.infrastructure.repositories.auth.role_permission import AlchemyRolePermissionRepository
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.application.use_cases.seed.seed_default_roles import SeedDefaultRoles
from app.application.use_cases.seed.seed_default_titles import SeedDefaultTitles
from app.application.use_cases.seed.seed_default_role_permissions import SeedDefaultRolePermissions


def run() -> None:
    with db_session() as db:
        # order matters: role_permission rows have a FK to roles
        SeedDefaultRoles(AlchemyRoleRepository(db)).execute()
        SeedDefaultTitles(AlchemyTitleRepository(db)).execute()
        SeedDefaultRolePermissions(
            AlchemyRolePermissionRepository(db),
            SystemTimeProvider(),
        ).execute()


if __name__ == "__main__":
    run()
