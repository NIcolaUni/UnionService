from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class SettoreMerceologicoDBmodel(database.Model):
    __tablename__ = "settore_merceologico"

    nome = Column(String(150), primary_key=True)


    def commitSettore(newRow):
        database.session.add(newRow)
        database.session.commit()

    def commitEliminaSettore(oldRow):
        database.session.delete(oldRow)
        databas