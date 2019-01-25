from sqlalchemy import Column, String, Float, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class ContabilitaCantiereDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "contabilita_cantiere"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'revisione', 'tipologia_lavorazione'),
    )

    numero_preventivo = Column(Integer())
    revisione = Column(Integer())
    tipologia = Column
    tipologia_lavorazione = Column(String(500))
    ordine_lav = Column(Integer())
    budget = Column(Float())
    costi_effettivi = Column(Float())
    fattura = Column(Float())