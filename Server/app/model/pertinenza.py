from .db.pertinenzaDBmodel import PertinenzaDBmodel

class Pertinenza(PertinenzaDBmodel):

    def __init__(self, nome):
        self.nome = nome

    def registraPertinenza(nome):
        new = Pertinenza(nome=nome)
        PertinenzaDBmodel.commitPertinenza(new)

    def eliminaPertinenza(nome):
        toDel = Pertinenza.query.filter_by(nome=nome).first()
        PertinenzaDBmodel.commitEliminaPertinenza(toDel)