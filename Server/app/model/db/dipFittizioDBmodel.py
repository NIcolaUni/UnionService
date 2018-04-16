from sqlalchemy import String, Column
from app import database

class DipFittizioDBmodel(database.Model):
    __tablename__="dipendente_fittizio"
    username = Column(String(10), primary_key=True)
    password = Column(String(10), nullable=False)