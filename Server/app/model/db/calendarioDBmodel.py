from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class CalendarioDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "calendario"
    __table_args__ = (
        PrimaryKeyConstraint('dipendente', 'start_date', 'titolo', 'tipologia'),

        ForeignKeyConstraint(['dipendente'], ['dipendente.username'],
                             onupdate='CASCADE', ondelete='CASCADE'),

    )


    dipendente = Column(String(60))
    titolo = Column(String(120))
    start_date = Column(Date())
    end_date = Column(Date())
    luogo = Column(String(120))
    descrizione = Column(String(500))

    tipologia = Column(Boolean())  # true evento generico, false ferie personali

    id_evento = Column(
        Integer())  # potrebbe essere una chiave ma si e' preferito mantenere gli attributi; serve piu' per il codice client