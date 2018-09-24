from .db.prodottoPrezzarioDBmodel import ProdottoPrezzarioDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app
class ProdottoPrezzario(ProdottoPrezzarioDBmodel):

    def __init__(self,
                    nome,
                    tipologia, capitolato_modello = None, capitolato_marchio = None ):

        self.nome=nome
        self.tipologia=tipologia
        self.capitolato_modello =capitolato_modello
        self.capitolato_marchio=capitolato_marchio




    def registraProdotto( nome, tipologia, capitolato_modello = None, capitolato_marchio=None ):

        prodotto = ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).first()

        if prodotto is None:
            newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia, capitolato_modello = capitolato_modello,
                                                capitolato_marchio= capitolato_marchio)

            ProdottoPrezzarioDBmodel.addRow(newProdotto)


            if capitolato_modello is not None:
                ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).update(
                    {
                        'capitolato_modello': capitolato_modello,
                        'capitolato_marchio': capitolato_marchio
                    })
                ProdottoPrezzarioDBmodel.commit()


    def eliminaProdotto(nome, tipologia):

        toDel = ProdottoPrezzario.query.filter_by( nome=nome, tipologia=tipologia ).first()
        ProdottoPrezzarioDBmodel.delRow(toDel)

    def modificaProdotto( nome, tipologia, modifica ):


        ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).update( modifica )

        ProdottoPrezzarioDBmodel.commit()

    def elimina(self):
        ProdottoPrezzarioDBmodel.delRow(self)
