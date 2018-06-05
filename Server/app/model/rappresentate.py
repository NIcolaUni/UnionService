from .db.rappresentateDBmodel import RappresentanteDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
from app import server

class Rappresentante(RappresentanteDBmodel):

    def __init__(self, nome, azienda, telefono, email):
        self.nome=nome
        self.azienda=azienda
        self.telefono=telefono
        self.email=email


    def registraRappresentante(nome, azienda, telefono=None, email=None):
        newRap = Rappresentante(nome=nome, azienda=azienda, telefono=telefono, email=email)

        try:
            RappresentanteDBmodel.addRow(newRap)
        except exc.SQLAlchemyError as e:
            server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            RappresentanteDBmodel.rollback()
            raise RigaPresenteException("Il rappresentante inserito è già presente")


    def modificaRappresentante(oldNome, nome, azienda, telefono=None, email=None):
        Rappresentante.query.filter_by(nome=oldNome, azienda=azienda).update(
            {
                'nome': nome,
                'azienda': azienda,
                'telefono': telefono,
                'email': email,
            })

        RappresentanteDBmodel.commit()



    def eliminaRappresentante(nome, azienda):
        toDel = Rappresentante.query.filter_by(nome=nome, azienda=azienda).first()
        RappresentanteDBmodel.delRow(toDel)
