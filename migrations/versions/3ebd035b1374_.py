"""empty message

Revision ID: 3ebd035b1374
Revises: 850469fa21c2
Create Date: 2017-08-08 00:27:33.008429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ebd035b1374'
down_revision = '850469fa21c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('message_ciphertext', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('receiver_id', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'messages', 'users', ['receiver_id'], ['id'])
    op.create_foreign_key(None, 'messages', 'users', ['sender_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'timestamp')
    op.drop_column('messages', 'sender_id')
    op.drop_column('messages', 'receiver_id')
    op.drop_column('messages', 'message_ciphertext')
    # ### end Alembic commands ###