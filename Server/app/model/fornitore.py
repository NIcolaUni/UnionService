from .db.fornitoreDBmodel import FornitoreDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException


class Fornitore(FornitoreDBmodel):

    def __init__(self,
                    nome_gruppo):

        self.nome_gruppo=nome_gruppo

    def registraFornitore(  nome_gruppo ):

        nuovoFornitore=Fornitore( nome_gruppo=nome_gruppo)

        try:
            FornitoreDBmodel.commitFornitore(nuovoFornitore)
        except exc.SQLAlchemyError as e:
            FornitoreDBmodel.rollback()
            raise RigaPresenteException("Il fornitore inserito è già presente")