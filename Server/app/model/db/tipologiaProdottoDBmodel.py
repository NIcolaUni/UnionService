from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class tipologiaProdottoDBmodel(database.Model):

    __tablename__ = "tipologia_prodotto_prezzario"


    nome = Column(String(100), primary_key=True)

    def commitTipoProdotto(tipoProdotto):
        database.session.add(tipoProdotto)
        database.session.commit()

    def commitEliminaTipoProdotto(tipoProdotto):
        database.session.delete(tipoProdotto)
        database.session.commit()

    def rollback():
        database.session.rollback()