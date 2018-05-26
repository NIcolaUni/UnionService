from .db.tipologiaProdottoDBmodel import TipologiaProdottoDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
from app import server

class TipologiaProdotto(TipologiaProdottoDBmodel):

    def __init__(self, nome):
        self.nome=nome


    def registraTipologiaProdotto(nome):

        newTipo = TipologiaProdotto(nome)

        try:
            TipologiaProdottoDBmodel.commitTipoProdotto(newTipo)
        except exc.SQLAlchemyError as e:
            server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            TipologiaProdottoDBmodel.rollback()
            raise RigaPresenteException("Tipologia prodotto già presente")

    def modificaTipologiaProdotto(nome, oldNome):

        TipologiaProdotto.query.filter_by(nome=oldNome).update(

            {
                'nome': nome,
             }
        );

        TipologiaProdotto.commit()

    def eliminaTipologiaProdotto(nome):
        toDel = TipologiaProdotto.query.filter_by(nome=nome).first()

        TipologiaProdottoDBmodel.commitEliminaTipoProdotto(toDel)