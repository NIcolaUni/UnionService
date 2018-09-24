from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class PersonaleFornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "personale_fornitore"
    __table_args__ = (
            PrimaryKeyConstraint('nome', 'cognome', 'azienda_primo_gruppo', 'azienda_sotto_gruppo'),
            ForeignKeyConstraint(['azienda_primo_gruppo', 'azienda_sotto_gruppo'],
                                 ['fornitore.primo_gruppo', 'fornitore.sotto_gruppo'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
                    )

    nome = Column(String(100))
    cognome = Column(String(100))
    azienda_primo_gruppo = Column(String(150))
    azienda_sotto_gruppo = Column(String(150))
    telefono = Column(String(30))
    email = Column(String(200))
    ruolo= Column(String(100))


