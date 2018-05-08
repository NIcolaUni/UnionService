from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class ListinoArtigianiDBmodel(database.Model):
    __tablename__="listinoartigiani"

    settore =
    tipologia =
    larghezza =
    altezza =
    profondita =
    unitaMisura =
    prezzoMin =
    prezzoMax =
