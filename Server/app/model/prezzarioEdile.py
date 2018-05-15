from .db.prezzarioEdileDBmodel import PrezzarioEdileDBmodel

class PrezzarioEdile(PrezzarioEdileDBmodel):

    def __init__(self, settore, tipologia, larghezza=None, altezza=None, profondita=None, unitaMisura=None, prezzoMin=None, prezzoMax=None):
        self.settore = settore
        self.tipologia = tipologia
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita
        self.unitaMisura = unitaMisura
        self.prezzoMin = prezzoMin
        self.prezzoMax = prezzoMax