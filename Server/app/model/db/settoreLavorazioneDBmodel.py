from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class SettoreLavorazioneDBmodel(database.Model):
    __tablename__ = "settore_lavorazione"

    nome = Column(String(100), primary_key=True)


    def commitSettore(nuovoSettore):
        database.session.add(nuovoSettore)
        database.session.commit()

    def commitEliminaSettore(settore):
        database.session.delete(settore)
        database.session.commit()