from .db.settoreLavorazioneDBmodel import SettoreLavorazioneDBmodel

class SettoreLavorazione(SettoreLavorazioneDBmodel):

    def __init__(self, nome):
        self.nome = nome


    def inizializza():
        if SettoreLavorazione.query.filter_by(nome='Non definito').first() is None:
            new = SettoreLavorazione(nome='Non definito')
            SettoreLavorazioneDBmodel.addRow(new)

    def registraSettore(nome):

        if SettoreLavorazione.query.filter_by(nome=nome).first() is None:
            new = SettoreLavorazione(nome=nome)
            SettoreLavorazioneDBmodel.addRow(new)

    def eliminaSettore(nome):
        toDel = SettoreLavorazione.query.filter_by(nome=nome).first()
        SettoreLavorazioneDBmodel.delRow(toDel)

    def modificaSettore(newNome, oldNome):
        SettoreLavorazioneDBmodel.query.filter_by(nome=oldNome).update({'nome': newNome})
        SettoreLavorazioneDBmodel.commit()