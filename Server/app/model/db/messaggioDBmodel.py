from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint, Time
from .dbUSinterface import DbUSinterface

class MessaggioDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "messaggio"
    __table_args__ = (
            PrimaryKeyConstraint('mittente', 'destinatario', 'data', 'ora'),
            ForeignKeyConstraint(['mittente'], ['dipendente.username'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['destinatario'], ['dirigente.username'],
                                 onupdate="CASCADE", ondelete="CASCADE")
                    )
    mittente = Column(String(60))
    destinatario = Column(String(60))
    testo = Column(String(1000), nullable=False)
    data = Column(Date())
    ora = Column(Time)
    letto = Column(Boolean)

