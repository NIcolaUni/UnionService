from sqlalchemy import String, Column, Boolean, ForeignKey
from app import database


class DipFittizioDBmodel(database.Model):
    __tablename__="dipendente_fittizio"
    username = Column(String(30), ForeignKey('dipendente_registrato.username'), primary_key=True )
    password = Column(String(30), nullable=False)
    classe = Column(String(20), nullable=False)
    dirigente = Column(Boolean, nullable=False)
    creatoreCredenziali = Column(String(60), ForeignKey('dirigente.username'))
   # dipReg = database.relationship("DipRegistratoDBmodel", uselist=False, back_populates="dipFittizio", single_parent=True)

    dipReg = database.relationship("DipRegistratoDBmodel", backref='dipFitt', lazy=True, uselist=False )
    dirigenteCreatore =  database.relationship("DirigenteDBmodel", backref='dipendenteAggiunto', lazy=True)