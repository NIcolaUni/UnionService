from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class CapitolatoProdottoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "capitolato_prodotto"
    __table_args__ = (
        PrimaryKeyConstraint('nome', 'modello', 'tipologia', 'marchio'),
        ForeignKeyConstraint(['nome', 'modello', 'tipologia', 'marchio'],
                             ['modello_prodotto_prezzario.prodotto',
                              'modello_prodotto_prezzario.nome',
                              'modello_prodotto_prezzario.tipologia',
                              'modello_prodotto_prezzario.marchio'],
                             onupdate="CASCADE", ondelete="CASCADE")
    )

    nome = Column(String(100))
    modello = Column(String(100))
    tipologia = Column(String(100))
    marchio = Column(String(100))
