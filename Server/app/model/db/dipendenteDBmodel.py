from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean
from app import database


class DipendenteDBmodel(database.Model):
    __tablename__ = "dipendente"
    username = Column(String(60), ForeignKey('dipendente_registrato.username'), primary_key=True, nullable=False)
    password =Column(String(30), ForeignKey('dipendente_registrato.password'), nullable=False)
    cf = Column(String(16), unique=True, nullable=False)
    nome = Column(String(30), nullable=False)
    cognome = Column(String(30), nullable=False)
    dataNascita = Column(Date(), nullable=False)
    residenza = Column(String(120), nullable=False)
    domicilio = Column(String(120))
    telefono = Column(String(12), nullable=False)
    email_aziendale = Column(String(50), nullable=False)
    email_personale = Column(String(50))
    iban = Column(String(30))
    partitaIva = Column(String(30))
    classe = Column(String(30), nullable=False)
    dirigente = Column(Boolean, nullable=False)
    session_id = Column(String(40), unique=True)
    regUser = database.relationship("DipRegistratoDBmodel", foreign_keys= [username])
    regPass = database.relationship("DipRegistratoDBmodel", foreign_keys=[password])
