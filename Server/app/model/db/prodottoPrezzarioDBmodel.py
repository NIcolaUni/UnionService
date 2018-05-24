from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class ProdottoPrezzarioDBmodel(database.Model):
    __tablename__ = "prodotto_prezzario"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'tipologia'),
            ForeignKeyConstraint(['fornitore_primo_gruppo', 'fornitore_sotto_gruppo'],
                                 ['sotto_gruppo_fornitori.gruppo_azienda', 'sotto_gruppo_fornitori.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['tipologia'], ['tipologia_prodotto_prezzario.nome'],
                                 onupdate="CASCADE", ondelete="SET NULL"),
             )

    nome = Column(String(100), primary_key=True)
    tipologia = Column(String(100))
    marchio = Column(String(100))
    codice = Column(String(100))
    fornitore_primo_gruppo = Column(String(150))
    fornitore_sotto_gruppo = Column(String(150))
    prezzoListino = Column(Integer())
    prezzoNettoListino = Column(Integer())
    rincaroNettoListino = Column(Integer())
    rincaroListino = Column(Integer())
    nettoUs = Column(Integer())
    rincaroTrasporto = Column(Integer())
    rincaroMontaggio = Column(Integer())
    scontoEx1 = Column(Integer())
    scontoEx2 = Column(Integer())
    scontoImballo = Column(Integer())
    rincaroTrasporto2 = Column(Integer())
    rincaroCliente = Column(Integer())


    def commitProdotto(prodotto):
        database.session.add(prodotto)
        database.session.commit()

    def commitEliminaProdotto(prodotto):
        database.session.delete(prodotto)
        database.session.commit()

    def rollback():
        database.session.rollback()