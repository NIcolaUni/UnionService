"""empty message

Revision ID: cc7beeddff11
Revises: 
Create Date: 2018-06-12 08:25:17.277183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc7beeddff11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('nome_cliente', sa.String(length=30), nullable=True),
    sa.Column('cognome_cliente', sa.String(length=30), nullable=True),
    sa.Column('indirizzo_cliente', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['nome_cliente', 'cognome_cliente', 'indirizzo_cliente'], ['cliente_accolto.nome', 'cliente_accolto.cognome', 'cliente_accolto.indirizzo'], ),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data')
    )
    op.create_table('lavorazione_preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('ordine', sa.Integer(), nullable=False),
    sa.Column('settore', sa.String(length=100), nullable=True),
    sa.Column('tipologia_lavorazione', sa.String(length=500), nullable=True),
    sa.Column('unitaMisura', sa.String(length=5), nullable=True),
    sa.Column('prezzoUnitario', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['numero_preventivo', 'data'], ['preventivo_edile.numero_preventivo', 'preventivo_edile.data'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data', 'ordine')
    )
    op.create_table('sottolavorazione_cad_preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('ordine', sa.Integer(), nullable=False),
    sa.Column('ordine_sottolavorazione', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'], ['lavorazione_preventivo_edile.numero_preventivo', 'lavorazione_preventivo_edile.data', 'lavorazione_preventivo_edile.ordine'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione')
    )
    op.create_table('sottolavorazione_mc_preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('ordine', sa.Integer(), nullable=False),
    sa.Column('ordine_sottolavorazione', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.Column('larghezza', sa.Float(), nullable=True),
    sa.Column('altezza', sa.Float(), nullable=True),
    sa.Column('profondita', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'], ['lavorazione_preventivo_edile.numero_preventivo', 'lavorazione_preventivo_edile.data', 'lavorazione_preventivo_edile.ordine'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione')
    )
    op.create_table('sottolavorazione_ml_preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('ordine', sa.Integer(), nullable=False),
    sa.Column('ordine_sottolavorazione', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.Column('larghezza', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'], ['lavorazione_preventivo_edile.numero_preventivo', 'lavorazione_preventivo_edile.data', 'lavorazione_preventivo_edile.ordine'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione')
    )
    op.create_table('sottolavorazione_mq_preventivo_edile',
    sa.Column('numero_preventivo', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('ordine', sa.Integer(), nullable=False),
    sa.Column('ordine_sottolavorazione', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.Column('larghezza', sa.Float(), nullable=True),
    sa.Column('altezza', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'], ['lavorazione_preventivo_edile.numero_preventivo', 'lavorazione_preventivo_edile.data', 'lavorazione_preventivo_edile.ordine'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sottolavorazione_mq_preventivo_edile')
    op.drop_table('sottolavorazione_ml_preventivo_edile')
    op.drop_table('sottolavorazione_mc_preventivo_edile')
    op.drop_table('sottolavorazione_cad_preventivo_edile')
    op.drop_table('lavorazione_preventivo_edile')
    op.drop_table('preventivo_edile')
    # ### end Alembic commands ###
