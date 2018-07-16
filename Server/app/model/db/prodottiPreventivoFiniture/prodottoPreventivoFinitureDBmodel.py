from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
import app

class ProdottoPreventivoFinitureDBmodel(app.database.Model):
    __tablename__ = "prodotto_preventivo_finiture"
    __table_args__ = (
            PrimaryKeyConstraint( 'numero_preventivo', 'data', 'tipologia', 'ordine' ),
            ForeignKeyConstraint(['numero_preventivo', 'data', 'tipologia'],
                                 ['preventivo.numero_preventivo', 'preventivo.data', 'preventivo.tipologia'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['tipologia', 'nome_prodotto', 'modello', 'marchio'],
                                 ['modello_prodotto_prezzario.tipologia',
                                  'modello_prodotto_prezzario.prodotto',
                                  'modello_prodotto_prezzario.nome',
                                  'modello_prodotto_prezzario.marchio'],
                                  ondelete='CASCADE', onupdate='CASCADE')
            )

    numero_preventivo = Column(Integer())
    data = Column(Date)
    ordine = Column(Integer()) # dov e' posizionata il prodotto nel preventivo

    tipologia = Column(String(100))
    nome_prodotto = Column(String(100))
    modello = Column(String(100))
    marchio = Column(String(100))
    codice = Column(String(100))
    quantita = Column(Float())
    unitaMisura = Column(String(5))
    diffCapitolato = Column(Float())



