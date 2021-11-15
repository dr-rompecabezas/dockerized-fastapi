"""add posts table

Revision ID: e9107ba8f6a3
Revises: 
Create Date: 2021-11-14 20:59:16.530070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9107ba8f6a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False), 
        sa.Column('title', sa.String(length=100), nullable=False), 
        sa.Column('content', sa.String(length=1000), nullable=False),
        sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'))
    pass

def downgrade():
    op.drop_table('posts')
    pass
