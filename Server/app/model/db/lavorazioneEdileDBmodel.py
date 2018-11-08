from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class LavorazioneEdileDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__="lavorazione_edile"

    __table_args__ = (
            PrimaryKeyConstraint('settore', 'tipologia_lavorazione'),
            )

    tipologia_lavorazione = Column(String(500))
    settore = Column(String(200),  ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="CASCADE"))
    pertinenza = Column(String(100), ForeignKey('settore_lavorazione.nome', onupdate="CASCADE", ondelete="SET DEFAULT"), server_default="Non definito")
    unitaMisura = Column(String(10))
    prezzoMin = Column(Float())
    prezzoMax = Column(Float())
    dimensione = Column(String(100))
    fornitura = Column(Float())
    posa = Column(Float())
    ricaricoAzienda = Column(Integer(), default=50)
    note = Column(String(500))
    daVerificare = Column(Boolean(), default=False)

