from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class SettoreLavorazioneDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "settore_lavorazione"

    nome = Column(String(100), primary_key=True)


