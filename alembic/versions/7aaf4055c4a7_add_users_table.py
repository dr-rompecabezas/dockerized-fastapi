"""add users table

Revision ID: 7aaf4055c4a7
Revises: e9107ba8f6a3
Create Date: 2021-11-14 21:01:45.945609

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.elements import False_


# revision identifiers, used by Alembic.
revision = '7aaf4055c4a7'
down_revision = 'e9107ba8f6a3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable=False), 
        sa.Column('email', sa.String(length=100), nullable=False), 
        sa.Column('password', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
