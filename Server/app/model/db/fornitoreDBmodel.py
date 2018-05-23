from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class FornitoreDBmodel(database.Model):
    __tablename__ = "fornitore"
    __table_args__ = (
            ForeignKeyConstraint(['settoreMerceologico'], ['settore_merceologico.nome'],
                                 onupdate="CASCADE", ondelete="SET NULL"),
                    )

    primo_gruppo = Column(String(150))
    sotto_gruppo = Column(String(150))
    settoreMerceologico = Column(String(150))
    tempiDiConsegna = Column(String(20))
    prezziNetti = Column(Boolean())
    scontoStandard = Column(Integer())
    scontoExtra1 = Column(Integer())
    scontroExtra2 = Column(Integer())
    trasporto = Column(Integer())
    trasportoUnitaMisura = Column(String(8))
    giorniPagamenti = Column(String(100))
    modalitaPagamenti = Column(String(100))
    tipologiaPagamenti = Column(String(100))
    provincia = Column(String(50))
    indirizzo = Column(String(150))
    telefono = Column(String(30))
    sito = Column(String(100))






    def commitSettore(newRow):
        database.session.add(newRow)
        database.session.commit()

    def commitEliminaSettore(oldRow):
        database.session.delete(oldRow)
        database.session.commit()