from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class TipologiaProdottoDBmodel(DbUSinterface, DbUSinterface.db.Model):

    __tablename__ = "tipologia_prodotto_prezzario"


    nome = Column(String(100), primary_key=True)
