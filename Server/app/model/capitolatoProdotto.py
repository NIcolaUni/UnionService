from .db.capitolatoProdottoDBmodel import CapitolatoProdottoDBmodel

class CapitolatoProdotto(CapitolatoProdottoDBmodel):

    def __init__(self, nome, modello, tipologia, marchio ):

        self.nome=nome
        self.modello=modello
        self.tipologia=tipologia
        self.marchio=marchio



    def registraCapitolato( nome, modello, tipologia, marchio ):

        oldCapitolato = CapitolatoProdotto.query.filter_by( tipologia=tipologia ).all()

        if oldCapitolato.__len__() > 0:
            for capitolato in oldCapitolato:
                CapitolatoProdotto.delRow(capitolato)

        prodotto = CapitolatoProdotto.query.filter_by(nome=nome, modello=modello, tipologia=tipologia, marchio=marchio).first()

        if prodotto is None:
            newProdotto = CapitolatoProdotto(nome=nome, modello=modello, tipologia=tipologia, marchio=marchio)

            CapitolatoProdotto.addRow(newProdotto)



    def eliminaCapitolato(nome, modello, tipologia, marchio):

        toDel = CapitolatoProdotto.query.filter_by(nome=nome, modello=modello, tipologia=tipologia, marchio=marchio ).first()
        CapitolatoProdotto.delRow(toDel)

    #def modificaCapitolato(nome, modello, tipologia, marchio ):
    #    CapitolatoProdotto.query.filter_by(nome=nome, modello=modello, tipologia=tipologia, marchio=marchio).update( modifica )

    #    CapitolatoProdotto.commit()


