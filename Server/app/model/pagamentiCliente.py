from .db.pagamentiClienteDBmodel import PagamentiClienteDBmodel

class PagamentiCliente(PagamentiClienteDBmodel):

    def __init__(self, numero_preventivo, totale_prev_edile=0, totale_prev_finiture=0, totale_prev_varianti=0, acconto=0, prima_rata=0,
                    prima_rata_pagata=False, seconda_rata=0, seconda_rata_pagata=False,
                    terza_rata=0, terza_rata_pagata=False, saldo=0):

        self.numero_preventivo = numero_preventivo
        self.totale_prev_edile = totale_prev_edile
        self.totale_prev_finiture = totale_prev_finiture
        self.totale_prev_varianti = totale_prev_varianti
        self.acconto = acconto
        self.prima_rata = prima_rata
        self.prima_rata_pagata = prima_rata_pagata
        self.seconda_rata = seconda_rata
        self.seconda_rata_pagata = seconda_rata_pagata
        self.terza_rata = terza_rata
        self.terza_rata_pagata = terza_rata_pagata
        self.saldo = saldo


    def generaPagamentoPerPreventivo(numero_preventivo):
        oldPag = PagamentiCliente.query.filter_by(numero_preventivo=numero_preventivo).first()

        if oldPag is None:
            newPag = PagamentiCliente(numero_preventivo=numero_preventivo)
            PagamentiClienteDBmodel.addRow(newPag)

    def ricalcolaRate(prev):

        totaleDaPagare = prev.totale_prev_edile+prev.totale_prev_finiture+prev.totale_prev_varianti

        if totaleDaPagare > 15000:
            acconto = totaleDaPagare*30/100
            prima_rata = (prev.totale_prev_edile*20/100)+(prev.totale_prev_finiture*50/100)
            seconda_rata= (prev.totale_prev_edile*20/100)+(prev.totale_prev_finiture*50/100)+(prev.totale_prev_varianti*50/100)
            terza_rata = (prev.totale_prev_edile*20/100)+(prev.totale_prev_varianti*50/100)
            saldo = 10


        else:

            acconto = totaleDaPagare * 50 / 100
            prima_rata = (prev.totale_prev_edile * 30 / 100) + prev.totale_prev_finiture + prev.totale_prev_varianti
            seconda_rata = 0
            terza_rata = 0
            saldo = 20

        PagamentiClienteDBmodel.query.filter_by(numero_preventivo=prev.numero_preventivo).update({
            'acconto' : acconto,
            'prima_rata' : prima_rata,
            'seconda_rata' : seconda_rata,
            'terza_rata': terza_rata,
            'saldo' : saldo

        })
        PagamentiClienteDBmodel.commit()


    def modificaPagamento(numero_preventivo, modifica):

        PagamentiClienteDBmodel.query.filter_by(numero_preventivo=numero_preventivo).update(modifica)
        PagamentiClienteDBmodel.commit()

        PagamentiCliente.ricalcolaRate(PagamentiClienteDBmodel.query.filter_by(numero_preventivo=numero_preventivo).first())