"""add content column to post table

Revision ID: 8cdd165df1e8
Revises: a56d5b5e3d07
Create Date: 2022-02-20 14:11:32.915412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cdd165df1e8'
down_revision = 'a56d5b5e3d07'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
