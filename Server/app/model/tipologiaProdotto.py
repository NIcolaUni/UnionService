from .db.tipologiaProdottoDBmodel import TipologiaProdottoDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app

class TipologiaProdotto(TipologiaProdottoDBmodel):

    def __init__(self, nome):
        self.nome=nome


    def registraTipologiaProdotto(nome):

        toTest = TipologiaProdotto.query.filter_by(nome=nome).first()

        if toTest is None:
            newTipo = TipologiaProdotto(nome)
            TipologiaProdottoDBmodel.addRow(newTipo)


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