from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class PrezzarioEdileDBmodel(database.Model):
    __tablename__="prezzario_edile"

    __table_args__ = (
            PrimaryKeyConstraint('settore', 'tipologia'),
            )

    settore = Column(String(30), ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="CASCADE"))
    tipologia = Column(String(30))
    larghezza = Column(Integer)
    altezza = Column(Integer)
    profondita = Column(Integer)
    unitaMisura = Column(String(5))
    prezzoMin = Column(Integer)
    prezzoMax = Column(Integer)
