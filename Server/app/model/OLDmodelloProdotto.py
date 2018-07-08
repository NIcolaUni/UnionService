from .db.modelloProdottoDBmodel import ModelloProdottoDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app

class ModelloProdotto(ModelloProdottoDBmodel):

    def __init__(self, nome, tipologia):
        self.nome=nome
        self.tipologia=tipologia


    def registraModelloProdotto(nome, tipologia):

        newTipo = ModelloProdotto(nome, tipologia)

        try:
            ModelloProdottoDBmodel.addRow(newTipo)
        except exc.SQLAlchemyError as e:
            ModelloProdottoDBmodel.rollback()
            raise RigaPresenteException("Modello prodotto già presente")

    def modificaModelloProdotto(modifica, oldNome, oldTipologia):

        ModelloProdotto.query.filter_by(nome=oldNome, tipologia=oldTipologia).update(modifica);

        ModelloProdotto.commit()

    def eliminaModelloProdotto(nome, tipologia):
        toDel = ModelloProdotto.query.filter_by(nome=nome, tipolgia=tipologia).first()

        ModelloProdottoDBmodel.delRow(toDel)

    def elimina(self):

        ModelloProdotto.delRow(self)

    def settaCapitolato(nome, tipologia, capitolato):
        ModelloProdotto.query.filter_by(nome=nome, tipologia=tipologia).update({'capitolato': capitolato});

        ModelloProdotto.commit()
