from .db.fornitoreDBmodel import FornitoreDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
from app import server

class Fornitore(FornitoreDBmodel):

    def __init__(self,
                    nome_gruppo, has_sottoGruppo=False):

        self.nome_gruppo=nome_gruppo
        self.has_sottoGruppo=has_sottoGruppo



    def registraFornitore(  nome_gruppo, has_sottoGruppo=False ):

        nuovoFornitore=Fornitore( nome_gruppo=nome_gruppo, has_sottoGruppo=has_sottoGruppo)

        try:
            FornitoreDBmodel.addRow(nuovoFornitore)
        except exc.SQLAlchemyError as e:
            server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            FornitoreDBmodel.rollback()
            raise RigaPresenteException("{}".format(e))

    def eliminaFornitore( nome ):

        toDel = Fornitore.query.filter_by(nome_gruppo=nome).first()
        FornitoreDBmodel.delRow(toDel)

    def setHas_sottoGruppi(fornitore, value):

        Fornitore.query.filter_by(nome_gruppo=fornitore).update(

            {
                'has_sottoGruppo': value
             }
        );

        Fornitore.commit()