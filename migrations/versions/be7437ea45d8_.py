"""empty message

Revision ID: be7437ea45d8
Revises: 3ebd035b1374
Create Date: 2017-08-08 00:33:32.871784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be7437ea45d8'
down_revision = '3ebd035b1374'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
