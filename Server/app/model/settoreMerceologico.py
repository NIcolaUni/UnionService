from .db.settoreMerceologicoDBmodel import SettoreMerceologicoDBmodel

class SettoreMerceologico(SettoreMerceologicoDBmodel):

    def __init__(self, nome):
        self.nome = nome



    def registraSettore(nome):

        aux = SettoreMerceologico.query.filter_by(nome=nome).first()

        if aux is None:
            new = SettoreMerceologico(nome=nome)
            SettoreMerceologicoDBmodel.addRow(new)

    def eliminaSettore(nome):
        toDel = SettoreMerceologico.query.filter_by(nome=nome).first()
        SettoreMerceologicoDBmodel.delRow(toDel)

    def modificaSettore(newNome, oldNome):
        SettoreMerceologico.query.filter_by(nome=oldNome).update({'nome': newNome})
        SettoreMerceologico.commit()