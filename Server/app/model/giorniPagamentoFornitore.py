from .db.giorniPagamentoFornitoreDBmodel import GiorniPagamentoFornitoreDBmodel


class GiorniPagamentoFornitore(GiorniPagamentoFornitoreDBmodel):

    def __init__(self, nome):
        self.nome = nome

    def registraGiorniPagamento(nome):

        if GiorniPagamentoFornitore.query.filter_by(nome=nome).first() is None:
            newRow = GiorniPagamentoFornitore(nome)
            GiorniPagamentoFornitoreDBmodel.addRow(newRow)

    def eliminaGiorniPagamento(nome):
        toDel = GiorniPagamentoFornitore.query.filter_by(nome=nome).first()
        GiorniPagamentoFornitoreDBmodel.delRow(toDel)

    def modificaGiorniPagamento(newNome, oldNome):

        GiorniPagamentoFornitore.query.filter_by(nome=oldNome).update({'nome': newNome })
        GiorniPagamentoFornitoreDBmodel.commit()