"""manager_id reference to  authorization

Revision ID: 43e3b2a2c4f2
Revises: d91b70b61a6a
Create Date: 2024-05-11 16:55:33.049941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43e3b2a2c4f2'
down_revision: Union[str, None] = 'd91b70b61a6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('application_manager_id_fkey', 'application', type_='foreignkey')
    op.drop_constraint('application_user_id_fkey', 'application', type_='foreignkey')
    op.drop_constraint('application_status_id_fkey', 'application', type_='foreignkey')
    op.create_foreign_key(None, 'application', 'status', ['status_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'application', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'application', 'authorization', ['manager_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('profile_update_application_application_id_fkey', 'profile_update_application', type_='foreignkey')
    op.create_foreign_key(None, 'profile_update_application', 'application', ['application_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'authorization', ['id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', schema='public', type_='foreignkey')
    op.create_foreign_key('user_id_fkey', 'user', 'authorization', ['id'], ['id'])
    op.drop_constraint(None, 'profile_update_application', schema='public', type_='foreignkey')
    op.create_foreign_key('profile_update_application_application_id_fkey', 'profile_update_application', 'application', ['application_id'], ['id'])
    op.drop_constraint(None, 'application', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'application', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'application', schema='public', type_='foreignkey')
    op.create_foreign_key('application_status_id_fkey', 'application', 'status', ['status_id'], ['id'])
    op.create_foreign_key('application_user_id_fkey', 'application', 'user', ['user_id'], ['id'])
    op.create_foreign_key('application_manager_id_fkey', 'application', 'user', ['manager_id'], ['id'])
    # ### end Alembic commands ###
