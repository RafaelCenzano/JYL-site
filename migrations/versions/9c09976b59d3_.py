"""empty message

Revision ID: 9c09976b59d3
Revises: 2836c70897ee
Create Date: 2020-02-23 22:02:01.752660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c09976b59d3'
down_revision = '2386c70897ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('firstname', sa.String(length=30), nullable=False))
    op.add_column('user', sa.Column('lastname', sa.String(length=30), nullable=False))
    op.add_column('user', sa.Column('nickname', sa.String(length=30), nullable=True))
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.drop_column('user', 'nickname')
    op.drop_column('user', 'lastname')
    op.drop_column('user', 'firstname')
    # ### end Alembic commands ###
