'''
from sqlalchemy import String, Column, Boolean, ForeignKey
from app import database

class SettimanaDBmodel(database.Model):
    __tablename__="disponibilita_settimanale"
    dipendente = Column(String(30), ForeignKey('dipendente.username'), primary_key=True)
    lunedi = Column(Boolean(), nullable=False)
    martedi = Column(Boolean(), nullable=False)
    mercoledi = Column(Boolean(), nullable=False)
    giovedi = Column(Boolean(), nullable=False)
    sabato = Column(Boolean(), nullable=False)
    domenica = Column(Boolean(), nullable=False)
    dip = database.relationship()
'''