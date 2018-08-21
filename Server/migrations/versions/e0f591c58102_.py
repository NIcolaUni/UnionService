"""empty message

Revision ID: e0f591c58102
Revises: ec8303dc1d2a
Create Date: 2018-08-01 16:00:05.064298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f591c58102'
down_revision = 'ec8303dc1d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calendario', sa.Column('end_date', sa.Integer(), nullable=True))
    op.drop_column('calendario', 'durata_giorni')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calendario', sa.Column('durata_giorni', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('calendario', 'end_date')
    # ### end Alembic commands ###
