from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class RappresentanteDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "rappresentante"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'azienda'),
            ForeignKeyConstraint(['azienda'], ['fornitore.nome_gruppo'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
                    )

    nome = Column(String(200))
    azienda = Column(String(150))
    telefono = Column(String(30))
    email = Column(String(200))


