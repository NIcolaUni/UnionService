from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ModelloProdottoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "modello_prodotto_prezzario"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'prodotto', 'tipologia', 'marchio'),
            ForeignKeyConstraint(['prodotto', 'tipologia'],
                                 ['prodotto_prezzario.nome', 'prodotto_prezzario.tipologia'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['fornitore_primo_gruppo', 'fornitore_sotto_gruppo'],
                                 ['fornitore.primo_gruppo', 'fornitore.sotto_gruppo'],
                                 onupdate="CASCADE", ondelete="CASCADE"),

            ForeignKeyConstraint(['tipologia'], ['tipologia_prodotto_prezzario.nome'],
                                 onupdate="CASCADE", ondelete="CASCADE")

             )

    nome = Column(String(100))
    prodotto = Column(String(100))
    tipologia = Column(String(100))
    marchio = Column(String(100))
    codice = Column(String(100))

    fornitore_primo_gruppo = Column(String(150))
    fornitore_sotto_gruppo = Column(String(150))

    prezzoListinoFornitura = Column(Float())


    rincaroAzienda = Column(Integer())
    trasportoAzienda = Column(Float())
    imballoAzienda = Column(Float())
    posa = Column(Float())
    posaPerc=Column(Integer())

    trasportoAziendaUnitaMisura = Column(String(8))
    imballoAziendaUnitaMisura = Column(String(8))

    nettoUsFornitura = Column(Float())


    rincaroCliente = Column(Integer())
    versoDiLettura = Column(Boolean()) #true da sinistra a destra, false viceversa
    daVerificare = Column(Boolean(), default=False)

