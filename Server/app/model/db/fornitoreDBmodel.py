from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class FornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model ):
    __tablename__ = "fornitore"
    __table_args__ = (
        PrimaryKeyConstraint('primo_gruppo', 'sotto_gruppo' ),
        ForeignKeyConstraint(['settoreMerceologico'], ['settore_merceologico.nome'],
                             ondelete='CASCADE', onupdate='CASCADE'),
        ForeignKeyConstraint(['giorniPagamenti'], ['giorni_pagamento_fornitore.nome'],
                             onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(['modalitaPagamenti'], ['modalita_pagamento_fornitore.nome'],
                             onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(['tipologiaPagamenti'], ['tipologia_pagamento_fornitore.nome'],
                             onupdate="CASCADE", ondelete="CASCADE"),
    )

    primo_gruppo = Column(String(150))
    sotto_gruppo = Column(String(150))
    settoreMerceologico = Column(String(150))
    stato = Column(String(100))
    tempiDiConsegna = Column(String(20))
    prezziNetti = Column(String(5))
    scontoStandard = Column(Integer())
    scontoExtra1 = Column(Integer())
    scontroExtra2 = Column(Integer(), default=0)
    trasporto = Column(Float())
    imballo = Column(Float())
    montaggio = Column(Float())
    trasportoUnitaMisura = Column(String(8))
    imballoUnitaMisura = Column(String(8))
    montaggioUnitaMisura = Column(String(8))
    giorniPagamenti = Column(String(100))
    modalitaPagamenti = Column(String(100))
    tipologiaPagamenti = Column(String(100))
    provincia = Column(String(50))
    indirizzo = Column(String(150))
    telefono = Column(String(30))
    sito = Column(String(100))
    daVerificare = Column(Boolean(), default=False)

