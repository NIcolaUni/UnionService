from sqlalchemy import Column, String
from .dbUSinterface import DbUSinterface


class TempiDiConsegnaFornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "tempi_di_consegna"

    nome = Column(String(100), primary_key=True)
