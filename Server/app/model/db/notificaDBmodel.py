from sqlalchemy import Column, String, ForeignKey
from app import database


class NotificaDBmodel(database.Model):
    __tablename__ = "notifica"
    dipendente = Column(String(60), ForeignKey('dipendente.username'), primary_key=True)
    titolo = Column(String(60), primary_key=True)
    contenuto = Column(String(500))

    destinatario = database.relationship('DipendenteDBmodel', backref='notifica', lazy=True, foreign_keys=[dipendente])
