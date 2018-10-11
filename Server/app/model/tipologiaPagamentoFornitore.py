from .db.tipologiaPagamentoFornitoreDBmodel import TipologiaPagamentoFornitoreDBmodel
import app

class TipologiaPagamentoFornitore(TipologiaPagamentoFornitoreDBmodel):

    def __init__(self, nome):
        self.nome=nome


    def registraTipologiaPagamento(nome):
        if TipologiaPagamentoFornitore.query.filter_by(nome=nome).first() is None:
            app.server.logger.info('\n\n\nwho {}\n\n'.format(nome))
            newRow = TipologiaPagamentoFornitore(nome=nome)
            TipologiaPagamentoFornitoreDBmodel.addRow(newRow)

    def eliminaTipologiaPagamento(nome):
        toDel = TipologiaPagamentoFornitore.query.filter_by(nome=nome).first()
        TipologiaPagamentoFornitoreDBmodel.delRow(toDel)

    def modificaTipologiaPagamento(newNome, oldNome):

        TipologiaPagamentoFornitore.query.filter_by(nome=oldNome).update({'nome': newNome })
        TipologiaPagamentoFornitoreDBmodel.commit()