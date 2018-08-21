"""empty message

Revision ID: 017ecbad2ceb
Revises: 01545762bd51
Create Date: 2018-08-01 12:55:55.818623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '017ecbad2ceb'
down_revision = '01545762bd51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agenda',
    sa.Column('dipendente', sa.String(length=60), nullable=False),
    sa.Column('titolo', sa.String(length=300), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('durata_giorni', sa.Integer(), nullable=True),
    sa.Column('start_hour', sa.Time(), nullable=True),
    sa.Column('durata_ore', sa.Integer(), nullable=True),
    sa.Column('cliente_sopraluogo', sa.String(length=60), nullable=True),
    sa.Column('accompagnatore_sopraluogo', sa.String(length=60), nullable=True),
    sa.Column('luogo_sopraluogo', sa.String(length=200), nullable=True),
    sa.Column('tipologia', sa.Boolean(), nullable=True),
    sa.Column('sopraluogo', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['dipendente'], ['dipendente.username'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('dipendente', 'start_date', 'titolo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('agenda')
    # ### end Alembic commands ###
