from flask_login import UserMixin
from app import login_manager
from app.model.db.dipendenteDBmodel import DipendenteDBmodel


class Dipendente(UserMixin, DipendenteDBmodel):

    def __init__(self, cf, nome, cognome, username, hash_passwd_login):
        self.cf = cf
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.hash_passwd_login = hash_passwd_login

    # Equivalente al toString() di java
    def __repr__(self):
        return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)

    def get_id(self):
        return self.cf

@login_manager.user_loader
def load_user(cf):
    return Dipendente.query.get(cf)
