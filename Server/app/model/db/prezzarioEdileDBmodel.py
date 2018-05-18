from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class PrezzarioEdileDBmodel(database.Model):
    __tablename__="prezzario_edile"

    __table_args__ = (
            PrimaryKeyConstraint('settore', 'tipologia_lavorazione'),
            )

    tipologia_lavorazione = Column(String(100))
    settore = Column(String(100), ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="SET NULL"))
    categoria = Column(String(100), ForeignKey('categoria_lavorazione.nome', onupdate="CASCADE", ondelete="SET NULL"))
    pertinenza = Column(String(100), ForeignKey('categoria_lavorazione.nome', onupdate="CASCADE", ondelete="SET NULL"))
    unitaMisura = Column(String(5))
    costo = Column(Integer)
    prezzoMin = Column(Integer)
    prezzoMax = Column(Integer)
    dimensione = Column(String(100))
    fornitura = Column(Integer)
    posa = Column(Integer)
    note = Column(String(500))
    daVerificare = Column(Boolean(), default=False)

    def commitLavorazione(lav):
        database.session.add(lav)
        database.session.commit()


    def commitEliminaLavorazione(lav):
        database.session.delete(lav)
        database.session.commit()

    def commit():
        database.session.commit()