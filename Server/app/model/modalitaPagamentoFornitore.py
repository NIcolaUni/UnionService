from .db.modalitaPagamentoFornitoreDBmodel import ModalitaPagamentoFornitoreDBmodel


class ModalitaPagamentoFornitore(ModalitaPagamentoFornitoreDBmodel):

    def __init__(self, nome):
        self.nome = nome

    def registraModalitaPagamento(nome):
        if ModalitaPagamentoFornitore.query.filter_by(nome=nome).first() is None:
            newRow = ModalitaPagamentoFornitore(nome)
            ModalitaPagamentoFornitoreDBmodel.addRow(newRow)

    def eliminaModalitaPagamento(nome):
        toDel = ModalitaPagamentoFornitore.query.filter_by(nome=nome).first()
        ModalitaPagamentoFornitoreDBmodel.delRow(toDel)

    def modificaModalitaPagamento(newNome, oldNome):

        ModalitaPagamentoFornitore.query.filter_by(nome=oldNome).update({'nome': newNome })
        ModalitaPagamentoFornitoreDBmodel.commit()