from sqlalchemy import Column, String, Float, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class ContabilitaCantiereDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "contabilita_cantiere"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'revisione', 'tipologia', 'ordine_lav'),
        ForeignKeyConstraint(['numero_preventivo', 'revisione', 'tipologia', 'ordine_lav'],
                              ['lavorazione_preventivo_edile.numero_preventivo', 'lavorazione_preventivo_edile.revisione',
                               'lavorazione_preventivo_edile.tipologia', 'lavorazione_preventivo_edile.ordine']),
        ForeignKeyConstraint(['nome_artigiano', 'impiego_artigiano'], ['artigiano.nominativo', 'artigiano.impiego'])
    )

    numero_preventivo = Column(Integer())
    revisione = Column(Integer())
    tipologia = Column(String(20))
    nome_lav = Column(String(1000))
    nome_artigiano = Column(String(60))
    impiego_artigiano = Column(String(60))
    ordine_lav = Column(Integer())
    budget = Column(Float())
    costi_effettivi = Column(Float())
    fattura = Column(Float())
    budget_imprevisti = Column(Float())
    fattura_budget_imprevisti = Column(Float())
