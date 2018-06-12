from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class SottolavorazioneMcDBmodel(app.database.Model):
    __tablename__ = "sottolavorazione_mc_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint(  'numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione'),
            ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine'],
                                 ['lavorazione_preventivo_edile.numero_preventivo',
                                  'lavorazione_preventivo_edile.data', 'lavorazione_preventivo_edile.ordine'],
                                 ondelete='CASCADE', onupdate='CASCADE')
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer())  # dov e' posizionata  la lavorazione nel preventivo
    ordine_sottolavorazione = Column(Integer())

    numero = Column(Integer())
    larghezza = Column(Float())
    altezza = Column(Float())
    profondita = Column(Float())

