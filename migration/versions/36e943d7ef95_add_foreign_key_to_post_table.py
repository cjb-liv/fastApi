"""add foreign key to post table

Revision ID: 36e943d7ef95
Revises: 9872c488c29e
Create Date: 2022-02-20 19:26:50.798633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36e943d7ef95'
down_revision = '9872c488c29e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'owner_id',
            sa.Integer(),
            nullable=False
            )
        )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
        )


def downgrade():
    op.drop_constraint('posts_users_fk','posts')
    op.drop_column('posts','owner_id')
