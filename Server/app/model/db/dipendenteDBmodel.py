from sqlalchemy import Column, String
from app import database

class Dipendente(database.Model):
    __tablename__ = "dipendente"
    cf = Column(String(16), primary_key=True)
    nome = Column(String(20), nullable=False)
    cognome = Column(String(30), nullable=False)
    username = Column(String(20), nullable=False)
    hash_passwd_login =Column(String(30), nullable=False)

    def __init__(self, cf, nome, cognome, username, hash_passwd_login):
        self.cf = cf
        self.nome = nome
        self.cognome = cognome
        self.username =username
        self.hash_passwd_login =hash_passwd_login

#Equivalente al toString() di java
    def __repr__(self):
        return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)