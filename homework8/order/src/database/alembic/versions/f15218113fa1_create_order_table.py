"""create order table

Revision ID: f15218113fa1
Revises: 
Create Date: 2023-10-04 17:17:09.179734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f15218113fa1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'order',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    pass
