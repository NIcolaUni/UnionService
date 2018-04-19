#from flask_login import UserMixin
#from app import login_manager
#from app import login_manager
from app.model.db.dipendenteDBmodel import DipendenteDBmodel


class Dipendente(DipendenteDBmodel):

    def __init__(self, cf, nome, cognome, username, password, sesso,
                 dataNascita, via, civico, cap, citta, regione, telefono, email_aziendale, email_personale,
                 iban, partitaIva, classe, dirigente):
        self.cf = cf
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.sesso = sesso
        self.dataNascita = dataNascita
        self.via = via
        self.civico = civico
        self.cap = cap
        self.citta = citta
        self.regione = regione
        self.telefono = telefono
        self.email_aziendale = email_aziendale
        self.email_personale = email_personale
        self.iban = iban
        self.partitaIva = partitaIva
        self.classe = classe
        self.dirigente = dirigente

    # Equivalente al toString() di java
    def __repr__(self):
        return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)
'''
    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return Dipendente.query.get(username)
'''