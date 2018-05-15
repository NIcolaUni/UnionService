from .db.settoreLavorazioneDBmodel import SettoreLavorazioneDBmodel

class SettoreLavorazione(SettoreLavorazioneDBmodel):

    def __init__(self, nome, categoria, pertinenza):
        self.nome = nome
        self.categoria = categoria
        self.pertinenza = pertinenza


    def registraSettore(nome, categoria, pertinenza):
        new = SettoreLavorazione(nome=nome, categoria=categoria, pertinenza=pertinenza)
        SettoreLavorazioneDBmodel.commitSettore(new)

    def eliminaSettore(nome):
        toDel = SettoreLavorazione.query.filter_by(nome=nome).first()
        SettoreLavorazioneDBmodel.commitEliminaSettore(toDel)