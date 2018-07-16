from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class CommessaDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "commessa_preventivo"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'intervento'),

    )

    numero_preventivo = Column(Integer())
    intervento = Column(String(120))
    indirizzo = Column(String(120))
    comune = Column(String(50))