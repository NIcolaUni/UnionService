from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class TipologiaProdottoDBmodel(database.Model):
    __tablename__ = "tipologia_prodotto"

    nome = Column(String(100), primary_key=True)

    def commitTipologiaProdotto(tipoProdotto):
        database.session.add(tipoProdotto)
        database.session.commit()

    def commitEliminaTipologiaProdotto(tipoProdotto):
        database.session.delete(tipoProdotto)
        database.session.commit()