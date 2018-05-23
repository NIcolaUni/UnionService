from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class RappresentanteDBmodel(database.Model):
    __tablename__ = "rappresentante"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'azienda'),
            ForeignKeyConstraint(['azienda'], ['fornitore.primo_gruppo'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
                    )

    nome = Column(String(200))
    azienda = Column(String(150))
    telefono = Column(String(30))
    email = Column(String(200))
    stato = Column(String(100))


    def commitSettore(newRow):
        database.session.add(newRow)
        database.session.commit()

    def commitEliminaSettore(oldRow):
        database.session.delete(oldRow)
        database.session.commit()