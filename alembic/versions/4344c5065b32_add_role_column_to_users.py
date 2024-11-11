"""add role column to users

Revision ID: 4344c5065b32
Revises: c4993db18bc4
Create Date: 2024-11-11 20:34:45.133190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4344c5065b32'
down_revision: Union[str, None] = 'c4993db18bc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
