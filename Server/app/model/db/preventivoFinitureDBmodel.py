from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class PreventivoFinitureDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "preventivo_finiture"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'data'),
        ForeignKeyConstraint(['nome_cliente', 'cognome_cliente', 'indirizzo_cliente'],
                             ['cliente_accolto.nome', 'cliente_accolto.cognome', 'cliente_accolto.indirizzo'],
                                onupdate='CASCADE', ondelete='CASCADE'),
        ForeignKeyConstraint(['dipendente_generatore'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='SET NULL'),
        ForeignKeyConstraint(['dipendente_ultimaModifica'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='SET NULL')
    )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    nome_cliente = Column(String(30))
    cognome_cliente = Column(String(30))
    indirizzo_cliente = Column(String(120))
    dipendente_generatore = Column(String(60))
    dipendente_ultimaModifica = Column(String(60))