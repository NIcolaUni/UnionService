from .db.tipologiaProdottoDBmodel import TipologiaProdottoDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app

class TipologiaProdotto(TipologiaProdottoDBmodel):

    def __init__(self, nome):
        self.nome=nome


    def registraTipologiaProdotto(nome):

        newTipo = TipologiaProdotto(nome)

        try:
            TipologiaProdottoDBmodel.addRow(newTipo)
        except exc.SQLAlchemyError as e:
            app.server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
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

        TipologiaProdottoDBmodel.delRow(toDel)

    def elimina(self):

        TipologiaProdotto.delRow(self)