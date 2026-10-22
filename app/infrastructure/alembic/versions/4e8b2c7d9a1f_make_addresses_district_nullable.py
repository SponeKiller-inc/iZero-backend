"""make addresses.district nullable (not every address has a municipal part)

Revision ID: 4e8b2c7d9a1f
Revises: c145e8b11823
Create Date: 2026-10-10 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4e8b2c7d9a1f'
down_revision: str | None = 'c145e8b11823'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'addresses', 'district',
        existing_type=sa.String(length=48),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Fall back to the city for addresses without a district, so the
    # NOT NULL constraint can be restored.
    op.execute("UPDATE addresses SET district = city WHERE district IS NULL")
    op.alter_column(
        'addresses', 'district',
        existing_type=sa.String(length=48),
        nullable=False,
    )
