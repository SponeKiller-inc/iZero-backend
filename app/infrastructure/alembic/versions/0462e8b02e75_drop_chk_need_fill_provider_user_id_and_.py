"""drop chk_need_fill_provider_user_id and chk_need_fill_password

Revision ID: 0462e8b02e75
Revises: 809a68f2735f
Create Date: 2026-09-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0462e8b02e75'
down_revision: Union[str, None] = '809a68f2735f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # IF EXISTS covers both the literal name and the ck_users_ naming-convention variant.
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS chk_need_fill_provider_user_id")
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS chk_need_fill_password")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT chk_need_fill_password "
        "CHECK (provider != 'local' OR password IS NOT NULL)"
    )
    op.execute(
        "ALTER TABLE users ADD CONSTRAINT chk_need_fill_provider_user_id "
        "CHECK (provider = 'local' OR provider_user_id IS NOT NULL)"
    )
