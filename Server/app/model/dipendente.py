from flask_login import UserMixin
from app import login_manager
from app.model.db.dipendenteDBmodel import DipendenteDBmodel


class Dipendente(UserMixin, DipendenteDBmodel):

    def __init__(self, cf, nome, cognome, username, password, sesso,
                 dataNascita, via, civico, cap, citta, regione, telefono, email, pass_email, IBAN, partitaIva):
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
        self.email = email
        self.pass_email = pass_email
        self.IBAN = IBAN
        self.partitaIva = partitaIva

    # Equivalente al toString() di java
    def __repr__(self):
        return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return Dipendente.query.get(username)
