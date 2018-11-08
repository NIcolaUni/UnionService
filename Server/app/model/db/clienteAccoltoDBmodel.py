from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ClienteAccoltoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "cliente_accolto"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'cognome', 'indirizzo'),
            )
    nome = Column(String(30))
    cognome = Column(String(30))
    indirizzo = Column(String(120))
    telefono = Column(String(12), nullable=False)
    email = Column(String(50), nullable=False)
    difficolta = Column(String(30), nullable=False)
    tipologia = Column(String(30), nullable=False)
    referenza = Column(String(30), nullable=False)
    sopraluogo = Column(Boolean(), nullable=False)
    datasopraluogo = Column(Date())
    lavorazione = Column(String(500), nullable=False)
    commerciale = Column(String(60), ForeignKey('dipendente_registrato.username', onupdate="CASCADE"), nullable=False)
    tecnico = Column(String(60), ForeignKey('dipendente_registrato.username',  onupdate="CASCADE", ondelete="SET NULL"))
    capocantiere = Column(String(60), ForeignKey('dipendente_registrato.username',  onupdate="CASCADE", ondelete="SET NULL"))
