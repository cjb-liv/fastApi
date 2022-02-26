"""add published and created at columns to post table

Revision ID: be500cccb317
Revises: 36e943d7ef95
Create Date: 2022-02-20 19:46:10.744584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be500cccb317'
down_revision = '36e943d7ef95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=sa.text('NOW()')
            ))
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        )

    )    
        

def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
