"""empty message

Revision ID: 8b93720020af
Revises: e18120394b9f
Create Date: 2018-07-17 09:55:47.185786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b93720020af'
down_revision = 'e18120394b9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prodotto_preventivo_finiture', sa.Column('tipologia_preventivo', sa.String(length=20), nullable=True))
    op.drop_constraint('prodotto_preventivo_finiture_numero_preventivo_fkey', 'prodotto_preventivo_finiture', type_='foreignkey')
    op.create_foreign_key(None, 'prodotto_preventivo_finiture', 'preventivo', ['numero_preventivo', 'data', 'tipologia_preventivo'], ['numero_preventivo', 'data', 'tipologia'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'prodotto_preventivo_finiture', type_='foreignkey')
    op.create_foreign_key('prodotto_preventivo_finiture_numero_preventivo_fkey', 'prodotto_preventivo_finiture', 'preventivo', ['numero_preventivo', 'data', 'tipologia'], ['numero_preventivo', 'data', 'tipologia'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('prodotto_preventivo_finiture', 'tipologia_preventivo')
    # ### end Alembic commands ###
