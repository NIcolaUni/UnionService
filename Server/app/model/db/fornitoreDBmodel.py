from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database



class FornitoreDBmodel(database.Model):
    __tablename__ = "fornitore"
    __table_args__ = (
            PrimaryKeyConstraint('nome_gruppo'),
                  )

    nome_gruppo = Column(String(150))



    def commitFornitore(newRow):
        database.session.add(newRow)
        database.session.commit()

    def commitEliminaFornitore(oldRow):
        database.session.delete(oldRow)
        database.session.commit()

    def rollback():
        database.session.rollback()