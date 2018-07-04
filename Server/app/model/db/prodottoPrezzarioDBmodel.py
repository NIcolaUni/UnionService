from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ProdottoPrezzarioDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "prodotto_prezzario"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'tipologia'),
            ForeignKeyConstraint(['fornitore_primo_gruppo', 'fornitore_sotto_gruppo'],
                                 ['sotto_gruppo_fornitori.gruppo_azienda', 'sotto_gruppo_fornitori.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['tipologia'], ['tipologia_prodotto_prezzario.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['modello', 'tipologia'], ['modello_prodotto_prezzario.nome', 'modello_prodotto_prezzario.tipologia'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
             )

    nome = Column(String(100))
    tipologia = Column(String(100))
    marchio = Column(String(100))
    codice = Column(String(100))
    modello = Column(String(200))
    fornitore_primo_gruppo = Column(String(150))
    fornitore_sotto_gruppo = Column(String(150))

    prezzoListinoFornituraPosa = Column(Float())
    prezzoListinoFornitura = Column(Float())


    rincaroAzienda = Column(Integer())
    trasportoAzienda = Column(Float())
    imballoAzienda = Column(Float())
    posa = Column(Float())

    trasportoAziendaUnitaMisura = Column(String(8))
    imballoAziendaUnitaMisura = Column(String(8))

    nettoUsFornituraPosa = Column(Float())
    nettoUsFornitura = Column(Float())


    rincaroCliente = Column(Integer())
    versoDiLettura = Column(Boolean()) #true da sinistra a destra, false viceversa
    daVerificare = Column(Boolean(), default=False)

