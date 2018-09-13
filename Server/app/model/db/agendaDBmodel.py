from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint, Time
from .dbUSinterface import DbUSinterface


class AgendaDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "agenda"
    __table_args__ = (
        PrimaryKeyConstraint('dipendente', 'giorno', 'inizio_ora'),

        ForeignKeyConstraint(['dipendente'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='CASCADE'),

    )

    dipendente = Column(String(60))
    titolo = Column(String(300))
    giorno = Column(Date())
    inizio_ora = Column(Time())
    fine_ora = Column(Time())
    cliente_sopraluogo = Column(String(60)) # stringa composta da "nome_cliente cognome_cliente"
    accompagnatore_sopraluogo = Column(String(60))
    luogo_sopraluogo = Column(String(200))

    #tipologia = Column(Boolean()) #true personale, false creata dal sistema
    sopraluogo = Column(Boolean(), default=False)

