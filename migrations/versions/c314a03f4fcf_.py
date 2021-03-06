"""empty message

Revision ID: c314a03f4fcf
Revises: 3d65c5d40f25
Create Date: 2017-08-07 23:46:12.294433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c314a03f4fcf'
down_revision = '3d65c5d40f25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('message_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'message_id')
    # ### end Alembic commands ###
