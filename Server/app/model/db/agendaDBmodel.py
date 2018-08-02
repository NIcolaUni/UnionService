from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint, Time
from .dbUSinterface import DbUSinterface


class AgendaDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "agenda"
    __table_args__ = (
        PrimaryKeyConstraint('dipendente', 'start_date', 'titolo'),

        ForeignKeyConstraint(['dipendente'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='CASCADE'),

    )

    dipendente = Column(String(60))
    titolo = Column(String(300))
    start_date = Column(Date)
    durata_giorni = Column(Integer())
    start_hour = Column(Time())
    durata_ore = Column(Integer())
    cliente_sopraluogo = Column(String(60)) # stringa composta da "nome_cliente cognome_cliente"
    accompagnatore_sopraluogo = Column(String(60))
    luogo_sopraluogo = Column(String(200))

    tipologia = Column(Boolean()) #true personale, false creata dal sistema
    sopraluogo = Column(Boolean(), default=False)

