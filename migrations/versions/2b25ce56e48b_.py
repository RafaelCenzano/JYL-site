"""empty message

Revision ID: 2b25ce56e48b
Revises: 39191dcd419c
Create Date: 2020-05-21 10:34:13.425000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b25ce56e48b'
down_revision = '39191dcd419c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'event', ['id'])
    op.create_unique_constraint(None, 'meeting', ['id'])
    op.add_column('user', sa.Column('numberphone', sa.String(length=10), nullable=True))
    op.drop_constraint('user_phoneareacode_key', 'user', type_='unique')
    op.drop_constraint('user_phoneend_key', 'user', type_='unique')
    op.drop_constraint('user_phonemiddle_key', 'user', type_='unique')
    op.create_unique_constraint(None, 'user', ['id'])
    op.drop_column('user', 'phonemiddle')
    op.drop_column('user', 'phoneareacode')
    op.drop_column('user', 'phoneend')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phoneend', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('phoneareacode', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('phonemiddle', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_unique_constraint('user_phonemiddle_key', 'user', ['phonemiddle'])
    op.create_unique_constraint('user_phoneend_key', 'user', ['phoneend'])
    op.create_unique_constraint('user_phoneareacode_key', 'user', ['phoneareacode'])
    op.drop_column('user', 'numberphone')
    op.drop_constraint(None, 'meeting', type_='unique')
    op.drop_constraint(None, 'event', type_='unique')
    # ### end Alembic commands ###
