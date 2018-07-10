from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ProdottoPrezzarioDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "prodotto_prezzario"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'tipologia'),
            ForeignKeyConstraint(['tipologia'], ['tipologia_prodotto_prezzario.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE")
             )

    nome = Column(String(100))
    tipologia = Column(String(100))
    capitolato_modello = Column(String(100))
    capitolato_marchio = Column(String(100))



