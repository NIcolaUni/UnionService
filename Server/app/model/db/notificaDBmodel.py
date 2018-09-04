from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint, Integer, Date, ForeignKeyConstraint
from .dbUSinterface import DbUSinterface

class NotificaDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "notifica"
    __table_args__ = (
            PrimaryKeyConstraint('destinatario', 'numero'),

            ForeignKeyConstraint(['richiedente_ferie', 'start_date'], ['richiesta_ferie.dipendente', 'richiesta_ferie.start_date'],
                                 onupdate='CASCADE', ondelete='CASCADE'),
            )

    destinatario = Column(String(60), ForeignKey('dipendente.username',  onupdate="CASCADE", ondelete="CASCADE"))
    numero = Column(Integer())
    titolo = Column(String(60))
    contenuto = Column(String(500))
    tipologia = Column(String(60)) # usato per distinguere la provvenienza  (inteso come evento generatore) delle diverse notifiche
    richiedente_ferie = Column(String(60))
    start_date = Column(Date())

