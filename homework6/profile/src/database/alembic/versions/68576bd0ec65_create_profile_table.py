"""create profile table

Revision ID: 68576bd0ec65
Revises: 
Create Date: 2023-08-15 22:12:17.025525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68576bd0ec65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'profile',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('middle_name', sa.String, nullable=False),
        sa.Column('gender', sa.String, nullable=False),
        sa.Column('birthday', sa.Date, nullable=False),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('profile')
