"""empty message

Revision ID: 9ed4d9416108
Revises: 227d93dff907
Create Date: 2020-05-29 11:14:17.286001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed4d9416108'
down_revision = '227d93dff907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(length=500), nullable=True))
    op.add_column('user', sa.Column('showaddr', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'showaddr')
    op.drop_column('user', 'address')
    # ### end Alembic commands ###