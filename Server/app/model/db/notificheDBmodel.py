from sqlalchemy import Column, String, ForeignKey
from app import database


class NotificheDBmodel(database.Model):
    __tablename__ = "notifiche"
    dipendente = Column(String(60), ForeignKey('dipendente.username'), primary_key=True)
    titolo = Column(String(60), primary_key=True)
    contenuto = Column(String(120))
    dirigente = Column(String(60), ForeignKey('dipendente.username'))

    destinatario = database.relationship('DipendenteDBmodel', backref='notificaPersonale', lazy=True, foreign_keys=[dipendente], cascade="all, delete-orphan")
    mittente = database.relationship('DipendenteDBmodel', backref='notificaInviata', lazy=True, foreign_keys=[dirigente], cascade="all, delete-orphan")

