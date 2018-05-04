from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean
from app import database


class DirigenteDBmodel(database.Model):
    __tablename__ = "dirigente"
    username = Column(String(60), ForeignKey('dipendente.username'), primary_key=True, nullable=False)

    datiPersonali = database.relationship('DipendenteDBmodel', backref='listaDirigenti', lazy=True, uselist=False)
