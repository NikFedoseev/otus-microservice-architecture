"""create orders table

Revision ID: a3fafcb772be
Revises: 
Create Date: 2023-09-26 11:27:28.639289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3fafcb772be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table(
        'order',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('active', sa.Boolean, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('order')
