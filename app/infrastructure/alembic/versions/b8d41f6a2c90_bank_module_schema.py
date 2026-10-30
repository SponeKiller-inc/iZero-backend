"""bank module schema

Revision ID: b8d41f6a2c90
Revises: e4b7c2a91d3f
Create Date: 2026-10-28 20:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8d41f6a2c90'
down_revision: str | None = 'e4b7c2a91d3f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Bank seat is held directly by banks; the catalogue is seeded only after this revision
    op.add_column('banks', sa.Column('address_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f('fk_banks_address_id_addresses'),
        'banks',
        'addresses',
        ['address_id'],
        ['id'],
    )
    op.drop_table('bank_addresses')

    # A user can currently have only one bank account (BR-6), so the assignment has no validity;
    # dropping the columns drops their valid dates check constraint as well
    op.drop_column('user_bank_accounts', 'valid_from')
    op.drop_column('user_bank_accounts', 'valid_to')
    op.create_unique_constraint(
        op.f('uq_user_bank_accounts_user_id'),
        'user_bank_accounts',
        ['user_id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_user_bank_accounts_user_id'), 'user_bank_accounts', type_='unique')
    # server_default backfills existing assignments as valid from now on
    op.add_column(
        'user_bank_accounts',
        sa.Column('valid_from', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.add_column(
        'user_bank_accounts',
        sa.Column(
            'valid_to',
            sa.DateTime(timezone=True),
            server_default=sa.text("'3000-01-01 00:00:00+00'"),
            nullable=False,
        ),
    )
    op.alter_column('user_bank_accounts', 'valid_from', server_default=None)
    op.alter_column('user_bank_accounts', 'valid_to', server_default=None)
    op.create_check_constraint(
        op.f('ck_user_bank_accounts_valid_dates'),
        'user_bank_accounts',
        'valid_to > valid_from',
    )

    op.create_table('bank_addresses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address_type_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(timezone=True), nullable=False),
    sa.Column('valid_to', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint('valid_to > valid_from', name='ck_bank_addresses_valid_dates'),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['address_type_id'], ['address_types.id'], ),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_constraint(op.f('fk_banks_address_id_addresses'), 'banks', type_='foreignkey')
    op.drop_column('banks', 'address_id')
