"""empty message

Revision ID: 47609b355f75
Revises: bc7876f81064
Create Date: 2017-08-08 00:22:27.174198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47609b355f75'
down_revision = 'bc7876f81064'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('timestamp', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'timestamp')
    # ### end Alembic commands ###
