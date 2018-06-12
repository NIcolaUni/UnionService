from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class LavorazionePreventivoDBmodel(app.database.Model):
    __tablename__ = "lavorazione_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'data', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'data'],
                                 ['preventivo_edile.numero_preventivo', 'preventivo_edile.data'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer()) # dov e' posizionata  la lavorazione nel preventivo

    settore = Column(String(100))
    tipologia_lavorazione = Column(String(500))
    unitaMisura = Column(String(5))
    prezzoUnitario = Column(Float())

