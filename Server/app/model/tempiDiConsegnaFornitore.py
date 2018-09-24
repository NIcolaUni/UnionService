from .db.tempiDiConsegnaFornitoreDBmodel import TempiDiConsegnaFornitoreDBmodel

class TempiDiConsegnaFornitore(TempiDiConsegnaFornitoreDBmodel):

    def __init__(self, nome):
        self.nome = nome



    def registraTempiDiConsegna(nome):
        aux=TempiDiConsegnaFornitore.query.filter_by(nome=nome).first()

        if aux is None:
            new = TempiDiConsegnaFornitore(nome=nome)
            TempiDiConsegnaFornitoreDBmodel.addRow(new)

    def eliminaTempiDiConsegna(nome):
        toDel = TempiDiConsegnaFornitore.query.filter_by(nome=nome).first()
        TempiDiConsegnaFornitoreDBmodel.delRow(toDel)