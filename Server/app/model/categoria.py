from .db.categoriaDBmodel import CategoriaDBmodel

class Categoria(CategoriaDBmodel):

    def __init__(self, nome):
        self.nome = nome


    def registraCategoria(nome):
        new = Categoria(nome)
        CategoriaDBmodel.commitCategoria(new)

    def eliminaCategoria(nome):
        toDel = Categoria.query.filter_by(nome=nome).first()
        CategoriaDBmodel.commitEliminaCategoria(toDel)