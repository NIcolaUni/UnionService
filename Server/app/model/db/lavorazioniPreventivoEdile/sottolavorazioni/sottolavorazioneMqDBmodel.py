from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app


class SottolavorazioneMqDBmodel(app.database.Model):
    __tablename__ = "sottolavorazione_mq_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint(  'numero_preventivo', 'data', 'ordine', 'ordine_sottolavorazione', 'tipologia'),
            ForeignKeyConstraint(['numero_preventivo', 'data', 'ordine', 'tipologia'],
                                 ['lavorazione_preventivo_edile.numero_preventivo',
                                  'lavorazione_preventivo_edile.data',
                                  'lavorazione_preventivo_edile.ordine',
                                  'lavorazione_preventivo_edile.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE')
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer())  # dov e' posizionata  la lavorazione nel preventivo
    ordine_sottolavorazione = Column(Integer())
    tipologia = Column(String(20))

    numero = Column(Integer())
    larghezza = Column(Float())
    altezza = Column(Float())
    prezzoBase = Column(Float())
    ricarico = Column(Integer())



