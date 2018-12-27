from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class LavorazionePreventivoVariantiDBmodel(app.database.Model):
    __tablename__ = "lavorazione_preventivo_varianti"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'revisione', 'tipologia', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'revisione', 'tipologia'],
                                 ['preventivo.numero_preventivo', 'preventivo.revisione', 'preventivo.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            )

    numero_preventivo = Column(Integer())
    revisione = Column(Integer())
    ordine = Column(Integer()) # dov e' posizionata  la lavorazione nel preventivo
    tipologia = Column(String(20))

    settore = Column(String(100))
    tipologia_lavorazione = Column(String(500))
    unitaMisura = Column(String(5))
    prezzoUnitario = Column(Float())

