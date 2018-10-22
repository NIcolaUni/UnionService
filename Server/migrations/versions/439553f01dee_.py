"""empty message

Revision ID: 439553f01dee
Revises: 2bce9aca3259
Create Date: 2018-10-17 20:59:37.771212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '439553f01dee'
down_revision = '2bce9aca3259'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artigiano', sa.Column('colore', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artigiano', 'colore')
    # ### end Alembic commands ###
