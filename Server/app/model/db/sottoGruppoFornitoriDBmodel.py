from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class SottoGruppoFornitoriDBmodel(database.Model):
    __tablename__ = "sotto_gruppo_fornitori"
    __table_args__ = (
        PrimaryKeyConstraint('nome', 'gruppo_azienda' ),
        ForeignKeyConstraint(['gruppo_azienda'], ['fornitore.nome_gruppo'],
                             onupdate="CASCADE", ondelete="CASCADE"),
    )

    nome = Column(String(150))
    gruppo_azienda = Column(String(150))
    settoreMerceologico = Column(String(150))
    tempiDiConsegna = Column(String(20))
    prezziNetti = Column(String(3))
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
    daVerificare = Column(Boolean(), default=False)

    def commitSottoGruppo(newRow):
        database.session.add(newRow)
        database.session.commit()

    def commitEliminaSottoGruppo(newRow):
        database.session.delete(newRow)

    def rollback():
        database.session.rollback()
