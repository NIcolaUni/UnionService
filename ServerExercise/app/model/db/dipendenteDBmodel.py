from sqlalchemy import Column, String
from app import database

class DipendenteDBmodel(database.Model):
    __tablename__ = "dipendente"
    cf = Column(String(16), primary_key=True)
    nome = Column(String(20), nullable=False)
    cognome = Column(String(30), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    hash_passwd_login =Column(String(30), nullable=False)
