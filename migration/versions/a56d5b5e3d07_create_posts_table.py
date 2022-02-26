"""create posts table

Revision ID: a56d5b5e3d07
Revises: 
Create Date: 2022-02-18 22:17:12.915713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a56d5b5e3d07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    #staring from blank db, create first table.
    op.create_table(
        'posts',
        sa.Column('id',sa.Integer(),nullable = False, primary_key=True),
        sa.Column('title',sa.String(),nullable = False)
        )


def downgrade():
    op.drop_table('posts')
    pass
