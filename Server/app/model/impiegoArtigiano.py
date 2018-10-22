from .db.impiegoArtigianoDBmodel import ImpiegoArtigianoDBmodel


class ImpiegoArtigiano(ImpiegoArtigianoDBmodel):

    def __init__(self, nome):
        self.nome = nome

    def registraImpiego(nome):

        imp = ImpiegoArtigianoDBmodel.query.filter_by(nome=nome).first()

        if imp is None:
            newImp = ImpiegoArtigianoDBmodel(nome=nome)

            ImpiegoArtigianoDBmodel.addRow(newImp)

    def eliminaImpiego(nome):
        toDel = ImpiegoArtigianoDBmodel.query.filter_by(nome=nome).first()
        ImpiegoArtigianoDBmodel.delRow(toDel)

    def modificaImpiego(oldNome, newNome):
        ImpiegoArtigianoDBmodel.query.filter_by(nome=oldNome).update({'nome' : newNome});

        ImpiegoArtigianoDBmodel.commit()