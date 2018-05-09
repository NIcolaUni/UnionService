from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class SettoreLavorazioneDBmodel(database.Model):
    __tablename__ = "settore_lavorazione"

    nome = Column(String(30), primary_key=True)