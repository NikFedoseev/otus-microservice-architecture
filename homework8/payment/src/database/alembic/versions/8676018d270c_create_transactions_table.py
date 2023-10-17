"""create transactions  table

Revision ID: 8676018d270c
Revises: c8970461cb11
Create Date: 2023-10-07 16:37:52.778308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8676018d270c'
down_revision: Union[str, None] = 'c8970461cb11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'transaction',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cart_id', sa.Integer, nullable=False),
        sa.Column('operation', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('order_id', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('transaction')
