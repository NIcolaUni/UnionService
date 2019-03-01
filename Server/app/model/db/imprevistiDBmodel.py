from sqlalchemy import Column, String, Float, Integer, PrimaryKeyConstraint, ForeignKeyConstraint
from .dbUSinterface import DbUSinterface


class ImprevistiDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "imprevisti"
    __table_args__ = (
        PrimaryKeyConstraint( 'numero_preventivo', 'revisione', 'ordine'),
        ForeignKeyConstraint(['numero_preventivo', 'revisione', 'tipologia'],
                             ['preventivo.numero_preventivo', 'preventivo.revisione', 'preventivo.tipologia']),
        ForeignKeyConstraint(['nome_artigiano', 'impiego_artigiano'], ['artigiano.nominativo', 'artigiano.impiego'])

    )

    nome = Column(String(100))
    numero_preventivo  = Column(Integer())
    revisione = Column(Integer())
    tipologia = Column(String(10)) #necessario per la chiave ma sempre settato a edile
    ordine = Column(Integer())
    costo = Column(Float())
    costo_fattura = Column(Float())
    nome_artigiano = Column(String(60))
    impiego_artigiano = Column(String(60))
