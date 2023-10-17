"""add booked_courier_slot table

Revision ID: 7520505cb2c8
Revises: 919910e9a2f3
Create Date: 2023-10-14 19:35:05.212877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7520505cb2c8'
down_revision: Union[str, None] = '919910e9a2f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        'booked_courier_slot',
        sa.Column('courier_id', sa.Integer),
        sa.Column('order_id', sa.Integer),
        sa.Column('date_from', sa.DateTime, nullable=False),
        sa.Column('date_to', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('booked_courier_slot')
