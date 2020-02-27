"""empty message

Revision ID: 782c4eef1834
Revises: 9adef8564288
Create Date: 2020-02-26 22:03:33.137880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782c4eef1834'
down_revision = '9adef8564288'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('unsurevote', sa.Integer(), default=0))
    op.add_column('meeting', sa.Column('unsurevote', sa.Integer(), default=0))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meeting', 'unsurevote')
    op.drop_column('event', 'unsurevote')
    # ### end Alembic commands ###
