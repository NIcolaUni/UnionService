from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, ForeignKey, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class ArtigianoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "artigiano"
    __table_args__ = (
        PrimaryKeyConstraint('nominativo', 'impiego'),

    )

    nominativo = Column(String(60))
    impiego = Column(String(60), ForeignKey('impiego_artigiano.nome', onupdate="CASCADE", ondelete="CASCADE"))
    valutazione = Column(Integer())
    contatti1 = Column(String(20))
    contatti2 = Column(String(20))
    email = Column(String(120))
    note = Column(String(500))
    colore = Column(String(10), default='white')