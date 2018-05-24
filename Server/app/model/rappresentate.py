from .db.rappresentateDBmodel import RappresentanteDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException


class Rappresentante(RappresentanteDBmodel):

    def __init__(self, nome, azienda, telefono, email, stato):
        self.nome=nome
        self.azienda=azienda
        self.telefono=telefono
        self.email=email
        self.stato=stato


    def registraRappresentante(nome, azienda, telefono=None, email=None, stato=None):
        newRap = Rappresentante(nome=nome, azienda=azienda, telefono=telefono, email=email, stato=stato)

        try:
            RappresentanteDBmodel.commitRappresentante(newRap)
        except exc.SQLAlchemyError as e:
            RappresentanteDBmodel.rollback()
            raise RigaPresenteException("Il rappresentante inserito è già presente")



