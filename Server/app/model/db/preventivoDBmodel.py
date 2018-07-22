from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class PreventivoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "preventivo"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'data', 'tipologia'),
        ForeignKeyConstraint(['nome_cliente', 'cognome_cliente', 'indirizzo_cliente'],
                             ['cliente_accolto.nome', 'cliente_accolto.cognome', 'cliente_accolto.indirizzo'],
                                onupdate='CASCADE', ondelete='CASCADE'),
        ForeignKeyConstraint(['dipendente_generatore'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='SET NULL'),
        ForeignKeyConstraint(['dipendente_ultimaModifica'], ['dipendente.username'],
                                onupdate='CASCADE', ondelete='SET NULL'),
        ForeignKeyConstraint(['numero_preventivo', 'intervento_commessa'],
                             ['commessa_preventivo.numero_preventivo', 'commessa_preventivo.intervento'],
                             onupdate='CASCADE', ondelete='CASCADE')
    )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    nome_cliente = Column(String(30))
    cognome_cliente = Column(String(30))
    indirizzo_cliente = Column(String(120))
    dipendente_generatore = Column(String(60))
    dipendente_ultimaModifica = Column(String(60))
    intervento_commessa = Column(String(130))
    tipologia = Column(String(20)) # edile, finiture o varianti
    stato = Column(Boolean()) # true in lavorazione, false
    note = Column(String(500))