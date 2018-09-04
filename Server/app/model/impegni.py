from .db.impegniDBmodel import ImpegniDBmodel
from sqlalchemy import desc


class Impegni(ImpegniDBmodel):

    def __init__(self, dipendente, id, testo, dirigente, checkato=False):

        self.dipendente = dipendente
        self.id = id
        self.testo = testo
        self.dirigente = dirigente
        self.checkato = checkato


    def registraImpegni(dipendente, testo, dirigente=None):

        impegni_registrati=ImpegniDBmodel.query.filter_by(dipendente=dipendente).order_by(desc(ImpegniDBmodel.id)).first()
        numToReturn = 0

        if impegni_registrati == None:
            impegno = Impegni(dipendente=dipendente, id=0, testo=testo, dirigente=dirigente)

        else:
            impegno = Impegni(dipendente=dipendente, id=impegni_registrati.id+1, testo=testo, dirigente=dirigente)
            numToReturn = impegni_registrati.id+1

        ImpegniDBmodel.addRow(impegno)

        if dirigente:
            return ( numToReturn, dirigente )
        else:
            return (numToReturn, 'Personale')

    def eliminaImpegni(dipendente, id):

        impegno = ImpegniDBmodel.query.filter_by( dipendente=dipendente, id=id).first()
        ImpegniDBmodel.delRow(impegno)

    def check(dipendente, id):
        impegno = ImpegniDBmodel.query.filter_by(dipendente=dipendente, id=id).first()

        if impegno.checkato:
            ImpegniDBmodel.query.filter_by(dipendente=dipendente, id=id).update({'checkato': False})
        else:
            ImpegniDBmodel.query.filter_by(dipendente=dipendente, id=id).update({'checkato': True})

        ImpegniDBmodel.commit()