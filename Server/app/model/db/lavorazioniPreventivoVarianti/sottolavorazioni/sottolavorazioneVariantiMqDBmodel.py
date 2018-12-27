from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app


class SottolavorazioneVariantiMqDBmodel(app.database.Model):
    __tablename__ = "sottolavorazione_mq_preventivo_varianti"
    __table_args__ = (
            PrimaryKeyConstraint(  'numero_preventivo', 'revisione', 'ordine', 'ordine_sottolavorazione', 'tipologia'),
            ForeignKeyConstraint(['numero_preventivo', 'revisione', 'ordine', 'tipologia'],
                                 ['lavorazione_preventivo_varianti.numero_preventivo',
                                  'lavorazione_preventivo_varianti.revisione',
                                  'lavorazione_preventivo_varianti.ordine',
                                  'lavorazione_preventivo_varianti.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE')
            )

    numero_preventivo = Column(Integer())
    revisione = Column(Integer())
    ordine = Column(Integer())  # dov e' posizionata  la lavorazione nel preventivo
    ordine_sottolavorazione = Column(Integer())
    tipologia = Column(String(20))

    numero = Column(Integer())
    larghezza = Column(Float())
    altezza = Column(Float())



