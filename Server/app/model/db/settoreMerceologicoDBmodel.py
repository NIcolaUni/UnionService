from sqlalchemy import Column, String
from .dbUSinterface import DbUSinterface


class SettoreMerceologicoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "settore_merceologico"

    nome = Column(String(100), primary_key=True)
