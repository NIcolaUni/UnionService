from .db.impegniDBmodel import ImpegniDBmodel
from sqlalchemy import desc


class Impegni(ImpegniDBmodel):

    def __init__(self, dipendente, id, testo, dirigente):

        self.dipendente = dipendente
        self.id = id
        self.testo = testo
        self.dirigente = dirigente


    def registraImpegni(dipendente, testo, dirigente=None):

        impegni_registrati=ImpegniDBmodel.query.filter_by(dipendente=dipendente).order_by(desc(ImpegniDBmodel.id)).first()


        if impegni_registrati == None:
            impegno = Impegni(dipendente=dipendente, id=0, testo=testo, dirigente=dirigente)
        else:
            impegno = Impegni(dipendente=dipendente, id=impegni_registrati.id+1, testo=testo, dirigente=dirigente)

        ImpegniDBmodel.commitImpegni(impegno)

    def eliminaImpegni(dipendente, id):

        impegno = ImpegniDBmodel.query.filter_by( dipendente=dipendente, id=id)
        ImpegniDBmodel.eliminaImpegni(impegno)