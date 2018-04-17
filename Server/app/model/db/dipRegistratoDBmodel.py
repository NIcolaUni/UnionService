from sqlalchemy import String, Column, Boolean
from app import database


class DipRegistratoDBmodel(database.Model):
    __tablename__="dipendente_registrato"
    username = Column(String(30), primary_key=True )
    password = Column(String(30), nullable=False, unique=True)
    fittizio = Column(Boolean, nullable=False)
    dipFittizio = database.relationship("DipFittizioDBmodel", uselist=False, back_populates="dipReg")
  #  dipUser = database.relationship("DipendenteDBmodel",  back_populates="regUser")
   # dipPass = database.relationship("DipendenteDBmodel",  back_populates="regPass")
