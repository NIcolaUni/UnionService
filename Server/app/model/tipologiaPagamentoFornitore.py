from .db.tipologiaPagamentoFornitoreDBmodel import TipologiaPagamentoFornitoreDBmodel

class TipologiaPagamentoFornitore(TipologiaPagamentoFornitoreDBmodel):

    def __init__(self, nome):
        self.nome=nome


    def registraTipologiaPagamento(nome):
        if TipologiaPagamentoFornitore.query.filter_by(nome=nome).first() is None:
            newRow = TipologiaPagamentoFornitore(nome)
            TipologiaPagamentoFornitoreDBmodel.addRow(newRow)

    def eliminaTipologiaPagamento(nome):
        toDel = TipologiaPagamentoFornitore.query.filter_by(nome=nome).first()
        TipologiaPagamentoFornitoreDBmodel.delRow(toDel)

    def modificaTipologiaPagamento(newNome, oldNome):

        TipologiaPagamentoFornitore.query.filter_by(nome=oldNome).update({'nome': newNome })
        TipologiaPagamentoFornitoreDBmodel.commit()