from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface



class FornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "fornitore"
    __table_args__ = (
            PrimaryKeyConstraint('nome_gruppo'),
                  )

    nome_gruppo = Column(String(150))
    has_sottoGruppo = Column(Boolean(), default=False)
