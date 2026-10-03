"""align addresses table with address schema (external_id, country_id, typed fields)

Revision ID: 7d3f1a9c2b6e
Revises: fff92843aa8b
Create Date: 2026-10-03 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7d3f1a9c2b6e'
down_revision: str | None = 'fff92843aa8b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('uq_addresses_ruian_id', 'addresses', type_='unique')
    op.alter_column('addresses', 'ruian_id', new_column_name='external_id')
    op.alter_column(
        'addresses', 'building_number',
        existing_type=sa.Integer(),
        type_=sa.String(length=10),
        postgresql_using='building_number::varchar',
    )
    op.alter_column(
        'addresses', 'orientation_number',
        existing_type=sa.Integer(),
        type_=sa.String(length=10),
        existing_nullable=True,
        postgresql_using='orientation_number::varchar',
    )
    op.alter_column(
        'addresses', 'district',
        existing_type=sa.String(length=48),
        nullable=False,
    )
    op.alter_column(
        'addresses', 'postal_code',
        existing_type=sa.String(length=5),
        type_=sa.Integer(),
        postgresql_using='postal_code::integer',
    )
    op.add_column('addresses', sa.Column('country_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f('fk_addresses_country_id_countries'),
        'addresses', 'countries', ['country_id'], ['id'],
    )
    op.create_unique_constraint(
        'uq_addresses_external_id_country_id',
        'addresses', ['external_id', 'country_id'],
    )
    op.drop_column('addresses', 'number_type')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'addresses',
        sa.Column('number_type', sa.String(length=4), nullable=False, server_default='č.p.'),
    )
    op.alter_column('addresses', 'number_type', server_default=None)
    op.drop_constraint('uq_addresses_external_id_country_id', 'addresses', type_='unique')
    op.drop_constraint(op.f('fk_addresses_country_id_countries'), 'addresses', type_='foreignkey')
    op.drop_column('addresses', 'country_id')
    op.alter_column(
        'addresses', 'postal_code',
        existing_type=sa.Integer(),
        type_=sa.String(length=5),
        postgresql_using='postal_code::varchar',
    )
    op.alter_column(
        'addresses', 'district',
        existing_type=sa.String(length=48),
        nullable=True,
    )
    op.alter_column(
        'addresses', 'orientation_number',
        existing_type=sa.String(length=10),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using='orientation_number::integer',
    )
    op.alter_column(
        'addresses', 'building_number',
        existing_type=sa.String(length=10),
        type_=sa.Integer(),
        postgresql_using='building_number::integer',
    )
    op.alter_column('addresses', 'external_id', new_column_name='ruian_id')
    op.create_unique_constraint('uq_addresses_ruian_id', 'addresses', ['ruian_id'])
