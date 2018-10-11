from .db.prodottoPrezzarioDBmodel import ProdottoPrezzarioDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app
class ProdottoPrezzario(ProdottoPrezzarioDBmodel):

    def __init__(self,
                    nome,
                    tipologia ):

        self.nome=nome
        self.tipologia=tipologia



    def registraProdotto( nome, tipologia ):

        prodotto = ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).first()

        if prodotto is None:
            newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia)

            ProdottoPrezzarioDBmodel.addRow(newProdotto)



    def eliminaProdotto(nome, tipologia):

        toDel = ProdottoPrezzario.query.filter_by( nome=nome, tipologia=tipologia ).first()
        ProdottoPrezzarioDBmodel.delRow(toDel)

    def modificaProdotto( nome, tipologia, modifica ):


        ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).update( modifica )

        ProdottoPrezzarioDBmodel.commit()

    def elimina(self):
        ProdottoPrezzarioDBmodel.delRow(self)
