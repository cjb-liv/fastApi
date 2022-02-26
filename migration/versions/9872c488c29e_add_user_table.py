"""add user table

Revision ID: 9872c488c29e
Revises: 8cdd165df1e8
Create Date: 2022-02-20 19:09:12.868506

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9872c488c29e'
down_revision = '8cdd165df1e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',sa.Integer(),nullable=False,primary_key=True), #primary key set
        sa.Column('email',sa.String(),nullable=False,unique=True), #set unique
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('NOW()'),nullable=False),
    )



def downgrade():
    op.drop_table('users')
    pass
