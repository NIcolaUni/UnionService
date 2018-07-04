from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ModelloProdottoDBmodel(DbUSinterface, DbUSinterface.db.Model):

    __tablename__ = "modello_prodotto_prezzario"

    __table_args__ = (
            PrimaryKeyConstraint('nome', 'tipologia'),
            ForeignKeyConstraint(['tipologia'], ['tipologia_prodotto_prezzario.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['capitolato', 'tipologia'], ['prodotto_prezzario.nome', 'prodotto_prezzario.tipologia'],
                                 onupdate="CASCADE", ondelete="CASCADE")
                    )

    nome = Column(String(200), primary_key=True)
    tipologia = Column(String(100))
    capitolato = Column(String(100))