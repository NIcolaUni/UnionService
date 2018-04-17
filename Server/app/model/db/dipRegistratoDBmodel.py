from sqlalchemy import String, Column, Boolean
from app import database
from app.model.db.dipFittizioDBmodel import DipFittizioDBmodel

class DipFittizioDBmodel(database.Model):
    __tablename__="dipendente_registrato"
    username = Column(String(30), primary_key=True )
    password = Column(String(30), nullable=False)
    fittizio = Column(Boolean, nullable=False)
    dipFittizio = relationship("DipFittizioDBmodel", uselist=False, back_populates="dipReg", cascade="all, delete-orphan")

