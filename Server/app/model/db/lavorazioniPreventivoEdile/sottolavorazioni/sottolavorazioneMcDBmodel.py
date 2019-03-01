from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class SottolavorazioneMcDBmodel(app.database.Model):
    __tablename__ = "sottolavorazione_mc_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint(  'numero_preventivo', 'revisione', 'ordine', 'tipologia', 'ordine_sottolavorazione'),
            ForeignKeyConstraint(['numero_preventivo', 'revisione', 'ordine', 'tipologia'],
                                 ['lavorazione_preventivo_edile.numero_preventivo',
                                  'lavorazione_preventivo_edile.revisione',
                                  'lavorazione_preventivo_edile.ordine',
                                  'lavorazione_preventivo_edile.tipologia'],
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
    profondita = Column(Float())
    prezzoBase = Column(Float())
    ricarico = Column(Integer())

    nome_modificato = Column(String(1000))

