from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database

class CategoriaDBmodel(database.Model):
    __tablename__ = "categoria_lavorazione"

    nome = Column(String(100), primary_key=True)


    def commitCategoria(newCategoria):
        database.session.add(newCategoria)
        database.session.commit()

    def commitEliminaCategoria(categoria):
        database.session.delete(categoria)
        database.session.commit()