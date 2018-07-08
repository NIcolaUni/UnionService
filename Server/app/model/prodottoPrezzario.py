from .db.prodottoPrezzarioDBmodel import ProdottoPrezzarioDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app
class ProdottoPrezzario(ProdottoPrezzarioDBmodel):

    def __init__(self,
                    nome,
                    tipologia, capitolato = None ):

        self.nome=nome
        self.tipologia=tipologia
        self.capitolato=capitolato




    def registraProdotto( nome, tipologia, capitolato = None ):

        prodotto = ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).first()

        if prodotto is None:
            newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia, capitolato=capitolato)


            try:
                ProdottoPrezzarioDBmodel.addRow(newProdotto)
            except exc.SQLAlchemyError as e:
                app.server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
                ProdottoPrezzarioDBmodel.rollback()
                raise RigaPresenteException("Il prodotto inserito è già presente")

        elif capitolato is not None:
            ProdottoPrezzario.query.filter_by(nome=nome, tipologia=tipologia).update({'capitolato': capitolato})


    def eliminaProdotto(nome, tipologia):

        toDel = ProdottoPrezzario.query.filter_by( nome=nome, tipologia=tipologia ).first()
        ProdottoPrezzarioDBmodel.delRow(toDel)

    def modificaProdotto( modifica ):

        oldNome =modifica.pop('oldNome')
        tipologia=modifica.pop('tipologia')

        ProdottoPrezzario.query.filter_by(nome=oldNome, tipologia=tipologia).update( modifica )

        ProdottoPrezzarioDBmodel.commit()

    def elimina(self):
        ProdottoPrezzarioDBmodel.delRow(self)


