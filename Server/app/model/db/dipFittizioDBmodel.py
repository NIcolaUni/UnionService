from sqlalchemy import String, Column, Boolean
from app import database
from app.model.db.dipRegistratoDBmodel import DipRegistratoDBmodel

class DipFittizioDBmodel(database.Model):
    __tablename__="dipendente_fittizio"
    username = Column(String(30), primary_key=True, database.ForeignKey('dipReg.username'))
    password = Column(String(30), nullable=False)
    classe = Column(String(20), nullable=False)
    dirigente = Column(Boolean, nullable=False)
    dipReg = relationship("DipRegistratoDBmodel", uselist=False, back_populates="dipFittizio")
