from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class PrezzarioEdileDBmodel(database.Model):
    __tablename__="prezzario_edile"

    __table_args__ = (
            PrimaryKeyConstraint('settore', 'tipologia_lavorazione'),
            )

    tipologia_lavorazione = Column(String(500))
    settore = Column(String(200),  ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="CASCADE"))
    pertinenza = Column(String(100),  ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="CASCADE"))
    unitaMisura = Column(String(5))
    costo = Column(Float())
    prezzoMin = Column(Float())
    prezzoMax = Column(Float())
    dimensione = Column(String(100))
    fornitura = Column(Float())
    posa = Column(Float())
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