from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class PreventivoEdileDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "preventivo_edile"
    __table_args__ = (
        PrimaryKeyConstraint('numero_preventivo', 'data'),
        ForeignKeyConstraint(['nome_cliente', 'cognome_cliente', 'indirizzo_cliente'],
                             ['cliente_accolto.nome', 'cliente_accolto.cognome', 'cliente_accolto.indirizzo'])
    )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    nome_cliente = Column(String(30))
    cognome_cliente = Column(String(30))
    indirizzo_cliente = Column(String(120))
