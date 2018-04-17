from sqlalchemy import Column, String, ForeignKey
from app import database


class DipendenteDBmodel(database.Model):
    __tablename__ = "dipendente"
    username = Column(String(30), ForeignKey('dipendente_registrato.username'), primary_key=True, nullable=False)
    password =Column(String(30), ForeignKey('dipendente_registrato.password'), nullable=False)
    cf = Column(String(16), unique=True, nullable=False)
    nome = Column(String(20), nullable=False)
    cognome = Column(String(30), nullable=False)

    regUser = database.relationship("DipRegistratoDBmodel", foreign_keys= [username])
    regPass = database.relationship("DipRegistratoDBmodel", foreign_keys=[password])