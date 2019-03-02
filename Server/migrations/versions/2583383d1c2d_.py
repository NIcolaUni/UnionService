"""empty message

Revision ID: 2583383d1c2d
Revises: 3208bd60f7aa
Create Date: 2019-03-01 12:19:35.730168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2583383d1c2d'
down_revision = '3208bd60f7aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contabilita_cantiere', sa.Column('impiego_artigiano', sa.String(length=60), nullable=True))
    op.add_column('contabilita_cantiere', sa.Column('nome_artigiano', sa.String(length=60), nullable=True))
    op.create_foreign_key(None, 'contabilita_cantiere', 'artigiano', ['nome_artigiano', 'impiego_artigiano'], ['nominativo', 'impiego'])
    op.add_column('imprevisti', sa.Column('impiego_artigiano', sa.String(length=60), nullable=True))
    op.add_column('imprevisti', sa.Column('nome_artigiano', sa.String(length=60), nullable=True))
    op.create_foreign_key(None, 'imprevisti', 'artigiano', ['nome_artigiano', 'impiego_artigiano'], ['nominativo', 'impiego'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'imprevisti', type_='foreignkey')
    op.drop_column('imprevisti', 'nome_artigiano')
    op.drop_column('imprevisti', 'impiego_artigiano')
    op.drop_constraint(None, 'contabilita_cantiere', type_='foreignkey')
    op.drop_column('contabilita_cantiere', 'nome_artigiano')
    op.drop_column('contabilita_cantiere', 'impiego_artigiano')
    # ### end Alembic commands ###
