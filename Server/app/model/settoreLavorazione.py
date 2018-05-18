from .db.settoreLavorazioneDBmodel import SettoreLavorazioneDBmodel

class SettoreLavorazione(SettoreLavorazioneDBmodel):

    def __init__(self, nome, categoria):
        self.nome = nome
        self.categoria = categoria



    def registraSettore(nome, categoria):
        new = SettoreLavorazione(nome=nome, categoria=categoria)
        SettoreLavorazioneDBmodel.commitSettore(new)

    def eliminaSettore(nome):
        toDel = SettoreLavorazione.query.filter_by(nome=nome).first()
        SettoreLavorazioneDBmodel.commitEliminaSettore(toDel)