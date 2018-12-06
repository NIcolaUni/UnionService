from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class LavorazionePreventivoDBmodel(app.database.Model):
    __tablename__ = "lavorazione_preventivo_edile"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'data', 'tipologia', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'data', 'tipologia'],
                                 ['preventivo.numero_preventivo', 'preventivo.data', 'preventivo.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer()) # dov e' posizionata  la lavorazione nel preventivo
    tipologia = Column(String(20))

    settore = Column(String(100))
    tipologia_lavorazione = Column(String(500))
    nome_modificato = Column(String(500))
    unitaMisura = Column(String(10))
    prezzoUnitario = Column(Float())

