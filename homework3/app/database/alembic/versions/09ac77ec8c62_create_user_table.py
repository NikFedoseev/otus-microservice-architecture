"""create user table

Revision ID: 09ac77ec8c62
Revises: 
Create Date: 2023-06-28 14:58:55.655027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09ac77ec8c62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('username', sa.String(256), nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('phone', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user')
