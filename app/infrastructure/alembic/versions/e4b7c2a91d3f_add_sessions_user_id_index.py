"""add sessions user_id index

Revision ID: e4b7c2a91d3f
Revises: e4a7c2d9b1f3
Create Date: 2026-10-25 20:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e4b7c2a91d3f'
down_revision: str | None = 'e4a7c2d9b1f3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
