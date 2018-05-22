from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class ProdottoPrezzarioDBmodel(database.Model):
    __tablename__ = "prodotto_prezzario"

    nome = Column(String(100), primary_key=True)
    tipologia =
    marchio
    codice
    fornitore
    listino


    def commitTipologiaProdotto(tipoProdotto):
        database.session.add(tipoProdotto)
        database.session.commit()

    def commitEliminaTipologiaProdotto(tipoProdotto):
        database.session.delete(tipoProdotto)
        database.session.commit()