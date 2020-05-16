"""empty message

Revision ID: 5bea26c84ddc
Revises: f8184878c692
Create Date: 2020-05-16 16:32:26.626006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bea26c84ddc'
down_revision = 'f8184878c692'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('currentEventCount', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('currentMeetingCount', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('lifetimeEventCount', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('lifetimeMeetingCount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'lifetimeMeetingCount')
    op.drop_column('user', 'lifetimeEventCount')
    op.drop_column('user', 'currentMeetingCount')
    op.drop_column('user', 'currentEventCount')
    # ### end Alembic commands ###