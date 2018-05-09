from .db.settoreLavorazioneDBmodel import SettoreLavorazioneDBmodel

class SettoreLavorazione(SettoreLavorazioneDBmodel):

    def __init__(self, nome):
        self.nome = nome