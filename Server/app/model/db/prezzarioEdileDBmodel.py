from sqlalchemy import Column, String, Float, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class PrezzarioEdileDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__="prezzario_edile"

    ricaricoAzienda = Column(Integer(), primary_key=True, default=50)


