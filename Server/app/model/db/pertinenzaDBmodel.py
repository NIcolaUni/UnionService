from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class PertinenzaDBmodel(database.Model):
    __tablename__ = "pertinenza_lavorazione"

    nome = Column(String(100), primary_key=True)

    def commitPertinenza(pertinenza):
        database.session.add(pertinenza)
        database.session.commit()


    def commitEliminaPertinenza(pertinenza):
        database.session.delete(pertinenza)
        database.session.commit()