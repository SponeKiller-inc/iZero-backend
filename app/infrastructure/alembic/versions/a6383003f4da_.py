"""align sessions table with ValidityMixin (valid_from/valid_to)

Revision ID: a6383003f4da
Revises: 0462e8b02e75
Create Date: 2026-09-28 19:25:59.263496

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a6383003f4da'
down_revision: Union[str, None] = '0462e8b02e75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE sessions DROP CONSTRAINT IF EXISTS ck_expired_at_in_future")

    op.add_column('sessions', sa.Column('valid_from', postgresql.TIMESTAMP(timezone=True), nullable=True))
    op.alter_column('sessions', 'expired_at', new_column_name='valid_to')

    # backfill valid_from with created_at for existing rows so the column can become NOT NULL
    op.execute("UPDATE sessions SET valid_from = created_at WHERE valid_from IS NULL")
    op.alter_column('sessions', 'valid_from', nullable=False)

    op.create_check_constraint('ck_sessions_valid_dates', 'sessions', 'valid_to > valid_from')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('ck_sessions_valid_dates', 'sessions', type_='check')

    op.alter_column('sessions', 'valid_to', new_column_name='expired_at')
    op.drop_column('sessions', 'valid_from')

    op.create_check_constraint('ck_expired_at_in_future', 'sessions', 'expired_at > now()')
