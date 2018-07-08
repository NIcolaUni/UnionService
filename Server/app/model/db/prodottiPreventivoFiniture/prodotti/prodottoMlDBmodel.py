from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class ProdottoMlDBmodel(app.database.Model):
    __tablename__ = "prodotto_ml_preventivo_finiture"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'data', 'ordine', 'ordine_sottoprodotto'),
            ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'],
                                 ['prodotti_preventivo_finiture.numero_preventivo',
                                  'prodotti_preventivo_finiture.data', 'prodotti_preventivo_finiture.ordine'],
                                 ondelete='CASCADE', onupdate='CASCADE')
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer())  # dov e' posizionato il prodotto nel preventivo
    ordine_sottoprodotto = Column(Integer())

    numero = Column(Integer())
    larghezza = Column(Float())



