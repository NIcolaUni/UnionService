from sqlalchemy import String, Column, Boolean, UniqueConstraint
from app import database


class DipRegistratoDBmodel(database.Model):
    __tablename__="dipendente_registrato"
    __table_args__ = (
                        UniqueConstraint('username', 'password'),
                        )
    username = Column(String(30), primary_key=True )
    password = Column(String(30), nullable=False )
    fittizio = Column(Boolean, nullable=False)
