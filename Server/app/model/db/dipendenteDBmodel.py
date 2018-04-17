from sqlalchemy import Column, String, ForeignKey, Date, Integer
from app import database


class DipendenteDBmodel(database.Model):
    __tablename__ = "dipendente"
    username = Column(String(30), ForeignKey('dipendente_registrato.username'), primary_key=True, nullable=False)
    password =Column(String(30), ForeignKey('dipendente_registrato.password'), nullable=False)
    cf = Column(String(16), unique=True, nullable=False)
    nome = Column(String(20), nullable=False)
    cognome = Column(String(30), nullable=False)
    sesso = Column(String(1), nullable=False)
    dataNascita = Column(Date(), nullable=False)
    via = Column(String(30), nullable=False)
    civico = Column(Integer(), nullable=False)
    citta = Column(String(30), nullable=False)
    regione = Column(String(30), nullable=False)
    telefono = Column(Integer(), nullable=False)
    email = Column(String(30), nullable=False)
    pass_email = Column(String(30), nullable=False)
    IBAN = Column(String(30), nullable=False)
    partitaIva = Column(String(30), nullable=False)
    regUser = database.relationship("DipRegistratoDBmodel", foreign_keys= [username])
    regPass = database.relationship("DipRegistratoDBmodel", foreign_keys=[password])
