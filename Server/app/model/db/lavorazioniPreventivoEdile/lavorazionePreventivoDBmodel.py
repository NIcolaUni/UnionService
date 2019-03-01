from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class LavorazionePreventivoDBmodel(app.database.Model):
    __tablename__ = "lavorazione_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'revisione', 'tipologia', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'revisione', 'tipologia'],
                                 ['preventivo.numero_preventivo', 'preventivo.revisione', 'preventivo.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint( ['settore', 'tipologia_lavorazione'],
                                  ['lavorazione_edile.settore', 'lavorazione_edile.tipologia_lavorazione'],
                                  onupdate="CASCADE"),
            ForeignKeyConstraint(['numero_preventivo', 'revisione', 'tipologia', 'ordine_lav_originale'],
                                    ['lavorazione_preventivo_edile.numero_preventivo',
                                     'lavorazione_preventivo_edile.revisione',
                                        'lavorazione_preventivo_edile.tipologia',
                                        'lavorazione_preventivo_edile.ordine' ],  onupdate="CASCADE")
            )

    numero_preventivo = Column(Integer())
    revisione = Column(Integer())
    ordine = Column(Integer()) # dov e' posizionata  la lavorazione nel preventivo
    tipologia = Column(String(20))

    settore = Column(String(100))
    tipologia_lavorazione = Column(String(1000))
    nome_modificato = Column(String(1000))
    unitaMisura = Column(String(10))
    prezzoUnitario = Column(Float())
    assistenza = Column(String(500))
    costo_assistenza = Column(Float())
    tipo_costo_assistenza = Column(Boolean()) # true percentuale

    # attributi delle lavorazioni copia
    copia = Column(Boolean(), default=False) # true se e' una lavorazione copia
    ordine_lav_originale = Column(Integer())
    settore_lav_copia = Column(String(100))
