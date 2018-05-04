from sqlalchemy import Column, String, ForeignKey
from app import database


class ImpegnoDBmodel(database.Model):
    __tablename__="todoList"
    dipendente = Column(String(60), ForeignKey('dipendente.username'), primary_key=True)
    titolo = Column(String(60), primary_key=True)
    contenuto = Column(String(120))
    dirigente = Column(String(60), ForeignKey('dirigente.username'))

    destinatario = database.relationship('DipendenteDBmodel', backref='impegnoPersonale', lazy=True, foreign_keys=[dipendente])
    mittente = database.relationship('DirigenteDBmodel', backref='impegnoImposto', lazy=True, foreign_keys=[dirigente])

