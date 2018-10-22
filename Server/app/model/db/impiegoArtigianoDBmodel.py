from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class ImpiegoArtigianoDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "impiego_artigiano"
    __table_args__ = (
        PrimaryKeyConstraint('nome'),

    )

    nome = Column(String(60))
