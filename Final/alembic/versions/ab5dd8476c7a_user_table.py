"""User table

Revision ID: ab5dd8476c7a
Revises: 
Create Date: 2024-05-08 17:23:16.216853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab5dd8476c7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('iinbin', sa.String(length=12), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(length=64), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('birthplace', sa.String(length=256), nullable=False),
    sa.Column('nation', sa.String(length=64), nullable=False),
    sa.Column('sex', sa.String(length=16), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_user_id'), 'user', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_user_iinbin'), 'user', ['iinbin'], unique=True, schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_public_user_iinbin'), table_name='user', schema='public')
    op.drop_index(op.f('ix_public_user_id'), table_name='user', schema='public')
    op.drop_table('user', schema='public')
    # ### end Alembic commands ###