from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class ProdottiPreventivoDBmodel(app.database.Model):
    __tablename__ = "prodotti_preventivo_finiture"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'data', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'data'],
                                 ['preventivo_finiture.numero_preventivo', 'preventivo_finiture.data'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['fornitore_primo_gruppo', 'fornitore_sotto_gruppo'],
                                 ['sotto_gruppo_fornitori.gruppo_azienda', 'sotto_gruppo_fornitori.nome'])
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer()) # dov e' posizionata il prodotto nel preventivo

    tipologia = Column(String(100))
    nome_prodotto = Column(String(500))
    unitaMisura = Column(String(5))
    prezzoUnitario = Column(Float())
    fornitore_primo_gruppo = Column(String(150))
    fornitore_sotto_gruppo = Column(String(150))
    modello = Column(String(500))

