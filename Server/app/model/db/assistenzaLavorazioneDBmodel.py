from sqlalchemy import Column, String, Float, Boolean,Integer, ForeignKeyConstraint, ForeignKey, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class AssistenzaLavorazioneDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "assistenza_lavorazione"
    __table_args__ = (
        PrimaryKeyConstraint('nome', 'tipologia_lavorazione', 'settore'),
        ForeignKeyConstraint(['tipologia_lavorazione', 'settore'],
                             ['lavorazione_edile.tipologia_lavorazione', 'lavorazione_edile.settore'],
                             onupdate='CASCADE', ondelete='CASCADE'),
    )

    nome = Column(String(500))
    costo = Column(Float())
    prezzoPercentuale =Column(Boolean()) # true percentuale, false netto

    tipologia_lavorazione = Column(String(1000))
    settore = Column(String(200))