from .db.settoreLavorazioneDBmodel import SettoreLavorazioneDBmodel

class SettoreLavorazione(SettoreLavorazioneDBmodel):

    def __init__(self, nome):
        self.nome = nome

    def registraSettore(nome):
        new = SettoreLavorazione(nome)
        SettoreLavorazioneDBmodel.commitSettore(new)

    def eliminaSettore(nome):
        toDel = SettoreLavorazione.query.filter_by(nome=nome).first()
        SettoreLavorazioneDBmodel.commitEliminaSettore(toDel)