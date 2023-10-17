"""create user carts  table

Revision ID: c8970461cb11
Revises: 
Create Date: 2023-10-07 16:37:30.934697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8970461cb11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_cart',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cart_number', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('money_amount', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_cart")
