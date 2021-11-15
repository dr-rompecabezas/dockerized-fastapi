"""add fkey to posts table

Revision ID: 06f3cbbf83ef
Revises: 7aaf4055c4a7
Create Date: 2021-11-14 21:12:31.786969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06f3cbbf83ef'
down_revision = '7aaf4055c4a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_users', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('fk_posts_users', table_name='posts', type_='foreignkey')
    op.drop_column('posts', column_name='owner_id')
    pass
