from .db.preventivoFinitureDBmodel import PreventivoFinitureDBmodel
from .db.prodottiPreventivoFiniture.prodottiPreventivoDBmodel import ProdottiPreventivoDBmodel
from .db.prodottiPreventivoFiniture.prodotti.prodottoCadDBmodel import ProdottoCadDBmodel
from .db.prodottiPreventivoFiniture.prodotti.prodottoMlDBmodel import ProdottoMlDBmodel
from .db.prodottiPreventivoFiniture.prodotti.prodottoMqDBmodel import ProdottoMqDBmodel
from .db.prodottiPreventivoFiniture.prodotti.prodottoMcDBmodel import ProdottoMcDBmodel
from .clienteAccolto import ClienteAccolto
from sqlalchemy import desc, func
import datetime
import app
import os


class __ProdottoCadPreventivo__(ProdottoCadDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottoprodotto, numero):
        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottoprodotto = ordine_sottoprodotto

        self.numero = numero


class __ProdottoMlPreventivo__(ProdottoMlDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottoprodotto, numero, larghezza):
        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottoprodotto

        self.numero = numero
        self.larghezza = larghezza


class __ProdottoMqPreventivo__(ProdottoMqDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottoprodotto, numero, larghezza, altezza):
        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottoprodotto = ordine_sottoprodotto

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza


class __ProdottoMcPreventivo__(ProdottoMcDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottoprodotto, numero, larghezza, altezza,
                 profondita):
        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottoprodotto = ordine_sottoprodotto

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita


class __ProdottiPreventivo__(ProdottiPreventivoDBmodel):
    def __init__(self, numero_preventivo, data, ordine, tipologia, unitaMisura,
                 prezzoUnitario, nome_prodotto, fornitore_primo_gruppo, fornitore_sotto_gruppo, modello):

        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine

        self.tipologia = tipologia
        self.nome_prodotto = nome_prodotto
        self.unitaMisura = unitaMisura
        self.prezzoUnitario = prezzoUnitario
        self.fornitore_sotto_gruppo = fornitore_sotto_gruppo
        self.fornitore_primo_gruppo = fornitore_primo_gruppo
        self.modello = modello


class PreventivoFiniture(PreventivoFinitureDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, dipendente_ultimaModifica=None):

        self.numero_preventivo = numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore

        if dipendente_ultimaModifica is None:
            self.dipendente_ultimaModifica = dipendente_generatore
        else:
            self.dipendente_ultimaModifica = dipendente_ultimaModifica

    def calcolaCodicePreventivo(self):
        # recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year % 100

        # recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo) + dipendente + str(annoPreventivo)

    def registraPreventivo(nome_cliente, cognome_cliente, indirizzo_cliente,
                           dipendente_generatore):

        youngerPrev = PreventivoFiniture.query.order_by(desc(PreventivoFiniture.numero_preventivo)).first()
        lastNumPrev = 99

        # se ci sono gia' preventivi registrati prende il numero_preventivo del piu' recente
        if youngerPrev is not None:
            lastNumPrev = youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoFiniture(numero_preventivo=lastNumPrev + 1, data=oggi, nome_cliente=nome_cliente,
                                     cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore)

        PreventivoFinitureDBmodel.addRow(preventivo)

        return (lastNumPrev + 1, oggi)

    def eliminaPreventivo(numero_preventivo, data):

        toDel = PreventivoFinitureDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data).first()

        PreventivoFinitureDBmodel.delRow(toDel)

    def __duplicaSottoprodotti__(prodotti, unitaMisura):

        returnList = []

        if unitaMisura == 'cad':
            for prod in prodotti:
                newProd = __ProdottoCadPreventivo__(numero_preventivo=prod.numero_preventivo,
                                                                data=prod.data, ordine=prod.ordine,
                                                                ordine_sottoprodotto=prod.ordine_sottoprodotto,
                                                                numero=prod.numero)
                returnList.append(newProd)

        elif unitaMisura == 'ml':
            for prod in prodotti:
                newProd = __ProdottoMlPreventivo__(numero_preventivo=prod.numero_preventivo,
                                                               data=prod.data, ordine=prod.ordine,
                                                               ordine_sottoprodotto=prod.ordine_sottoprodotto,
                                                               numero=prod.numero, larghezza=prod.larghezza)
                returnList.append(newProd)

        elif unitaMisura == 'mq':
            for prod in prodotti:
                newProd = __ProdottoMqPreventivo__(numero_preventivo=prod.numero_preventivo,
                                                               data=prod.data, ordine=prod.ordine,
                                                               ordine_sottoprodotto=prod.ordine_sottoprodotto,
                                                               numero=prod.numero, larghezza=prod.larghezza,
                                                               altezza=prod.altezza)
                returnList.append(newProd)

        elif unitaMisura == 'mc':
            for prod in prodotti:
                newProd = __ProdottoMcPreventivo__(numero_preventivo=prod.numero_preventivo,
                                                               data=prod.data, ordine=prod.ordine,
                                                               ordine_sottoprodotto=prod.ordine_sottoprodotto,
                                                               numero=prod.numero, larghezza=prod.larghezza,
                                                               altezza=prod.altezza, profondita=prod.profondita)
                returnList.append(newProd)

        return returnList

    def __duplicaProdotti__(prodotti):

        app.server.logger.info("\n\nEntrato in duplica lav\n")

        returnList = []
        for prod in prodotti:
            newProd = __ProdottiPreventivo__(   numero_preventivo=prod.numero_preventivo, data=prod.data,
                                               ordine=prod.ordine,
                                               settore=prod.nome_prodotto, tipologia_lavorazione=prod.tipologia,
                                               unitaMisura=prod.unitaMisura, prezzoUnitario=prod.prezzoUnitario)
            returnList.append(newProd)

        return returnList

    def modificaPreventivo(numero_preventivo, dipendente_ultimaModifica):
        '''
         Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
         piu' recente, ne fa una copia ( compresa di lavorazioni e sottolavorazioni ) cambiando unicamente
         gli attributi "data", settata alla data odierna, e "dipendente_ultimaModifica", settato con lo username
         del dipendente che sta facendo la modifica.

        :param numero_preventivo, dipendente_ultimaModifica:
        :return:
        '''

        lastPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo).order_by(
            desc(PreventivoFiniture.data)).first()
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        # se il preventivo viene modificato piu' volte lo stesso giorno o viene modificato
        # il giorno non viene fatta alcuna copia e viene unicamente modificato
        # il parametro "dipendente_ultimaModifica"

        if str(now).split(' ')[0] == str(lastPrev.data):
            PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo).update(
                {'dipendente_ultimaModifica': dipendente_ultimaModifica.username})

            PreventivoFiniture.commit()

            return (numero_preventivo, oggi)

        preventivo = PreventivoFiniture(numero_preventivo=lastPrev.numero_preventivo, data=oggi,
                                     nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente,
                                     indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=lastPrev.dipendente_generatore,
                                     dipendente_ultimaModifica=dipendente_ultimaModifica.username)

        PreventivoFinitureDBmodel.addRow(preventivo)

        prodotti = __ProdottiPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo,
                                                                data=lastPrev.data).all()

        prodotti = PreventivoFiniture.__duplicaLavorazioni__(prodotti)

        for prod in prodotti:

            prod.data = oggi
            PreventivoFinitureDBmodel.addRowNoCommit(prod)

        PreventivoFiniture.commit()

        prodottiCad = __ProdottoCadPreventivo__.query.filter_by(
            numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        prodottiCad = PreventivoFiniture.__duplicaSottolavorazioni__(prodottiCad, 'cad')

        prodottiMl = __ProdottoMlPreventivo__.query.filter_by(
            numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        prodottiMl = PreventivoFiniture.__duplicaSottolavorazioni__(prodottiMl, 'ml')

        prodottiMq = __ProdottoMqPreventivo__.query.filter_by(
            numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        prodottiMq = PreventivoFiniture.__duplicaSottolavorazioni__(prodottiMq, 'mq')

        prodottiMc = __ProdottoMcPreventivo__.query.filter_by(
            numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        prodottiMc = PreventivoFiniture.__duplicaSottolavorazioni__(prodottiMc, 'mc')

        prodotti = prodottiCad + prodottiMl + prodottiMc + prodottiMq

        for sottoLav in prodotti:
            sottoLav.data = oggi
            PreventivoFinitureDBmodel.addRowNoCommit(sottoLav)

        PreventivoFiniture.commit()

        return (numero_preventivo, oggi)

    def __calcolcaOrdineSottoprodotto__(queryClass, numero_preventivo, data, ordine):
        ordine_sottoprodotto = 0

        aux = queryClass.filter_by(numero_preventivo=numero_preventivo, data=data,
                                   ordine=ordine, ordine_sottoprodotto=ordine_sottoprodotto).first()

        while aux is not None:
            ordine_sottoprodotto += 1
            aux = queryClass.filter_by(numero_preventivo=numero_preventivo, data=data,
                                       ordine=ordine, ordine_sottolavorazione=ordine_sottoprodotto).first()

        return ordine_sottoprodotto

    def __registraSottoprodotto__(numero_preventivo, data, ordine, ordine_sottoprodotto, unitaMisura,
                                     numero, larghezza=None, altezza=None, profondita=None):

        prodotto = None
        if unitaMisura == 'cad':
            prodotto = __ProdottoCadPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                            ordine=ordine,
                                                    ordine_sottoprodotto=ordine_sottoprodotto,
                                                            numero=numero)
        elif unitaMisura == 'ml':
            prodotto = __ProdottoMlPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                   ordine_sottoprodotto=ordine_sottoprodotto,
                                                           numero=numero, larghezza=larghezza)

        elif unitaMisura == 'mq':
            prodotto = __ProdottoMqPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                   ordine_sottoprodotto=ordine_sottoprodotto,
                                                           numero=numero, larghezza=larghezza, altezza=altezza)

        elif unitaMisura == 'mc':
            prodotto = __ProdottoMcPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                   ordine_sottoprodotto=ordine_sottoprodotto,
                                                           numero=numero, larghezza=larghezza, altezza=altezza,
                                                           profondita=profondita)

        PreventivoFinitureDBmodel.addRow(prodotto)

    def nuovaSottoprodotto(numero_preventivo, data, ordine):

        unitaMisura = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                ordine=ordine).first().unitaMisura

        if unitaMisura == 'cad':
            last_sottoprod_cad = __ProdottoCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                  data=data, ordine=ordine).order_by(
                desc(__ProdottiPreventivo__.ordine_sottoprodotto)).first().ordine_sottoprodotto

            PreventivoFiniture.__registraSottoprodotto__(numero_preventivo=numero_preventivo, data=data,
                                                         unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottoprodotto=last_sottoprod_cad + 1,
                                                         numero=1)
        elif unitaMisura == 'ml':
            last_sottoprod_ml = __ProdottoMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by(
                desc(__ProdottoMlPreventivo__.ordine_sottoprodotto)).first().ordine_sottoprodotto

            PreventivoFiniture.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data,
                                                         unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottoprodotto=last_sottoprod_ml + 1,
                                                         numero=1, larghezza=1)

        elif unitaMisura == 'mq':
            last_sottoprod_mq = __ProdottoMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by(
                desc(__ProdottoMqPreventivo__.ordine_sottoprodotto)).first().ordine_sottoprodotto

            PreventivoFiniture.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data,
                                                         unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottoprodotto=last_sottoprod_mq + 1,
                                                         numero=1, larghezza=1, altezza=1)


        elif unitaMisura == 'mc':
            last_sottoprod_mc = __ProdottoMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by(
                desc(__ProdottoMcPreventivo__.ordine_sottoprodotto)).first().ordine_sottoprodotto

            PreventivoFiniture.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data,
                                                         unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottoprodotto=last_sottoprod_mc + 1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1)

    def registraLavorazione(numero_preventivo, data, ordine, nome_prodotto, tipologia, unitaMisura,
                            prezzoUnitario, fornitore_primo_gruppo, fornitore_sotto_gruppo, modello,
                            numero, larghezza=None, altezza=None, profondita=None):

        controlVar = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                               ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:
            prodotto = __ProdottiPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                    ordine=ordine, nome_prodotto=nome_prodotto,
                                                    tipologia=tipologia,
                                                    unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario,
                                                    modello = modello,
                                                    fornitore_primo_gruppo=fornitore_primo_gruppo,
                                                    fornitore_sotto_gruppo=fornitore_sotto_gruppo)

            PreventivoFinitureDBmodel.addRow(prodotto)
        else:  # se la lavorazione e' gia' presente registra la sottolavorazione

            if unitaMisura == 'cad':
                ordineSottoProdotto = PreventivoFiniture.__calcolcaOrdineSottolavorazione__(
                    queryClass=__ProdottoCadPreventivo__.query,
                    numero_preventivo=numero_preventivo, data=data,
                    ordine=ordine)
            elif unitaMisura == 'ml':
                ordineSottoProdotto = PreventivoFiniture.__calcolcaOrdineSottolavorazione__(
                    queryClass=__ProdottoMlPreventivo__.query,
                    numero_preventivo=numero_preventivo, data=data,
                    ordine=ordine)

            elif unitaMisura == 'mq':
                ordineSottoProdotto = PreventivoFiniture.__calcolcaOrdineSottolavorazione__(
                    queryClass=__ProdottoMqPreventivo__.query,
                    numero_preventivo=numero_preventivo, data=data,
                    ordine=ordine)

            elif unitaMisura == 'mc':
                ordineSottoProdotto = PreventivoFiniture.__calcolcaOrdineSottolavorazione__(
                    queryClass=__ProdottoMcPreventivo__.query,
                    numero_preventivo=numero_preventivo, data=data,
                    ordine=ordine)

        PreventivoFiniture.__registraSottoprodotto__(numero_preventivo=numero_preventivo, data=data,
                                                     unitaMisura=unitaMisura,
                                                     ordine=ordine, ordine_sottoprodotto=ordineSottoProdotto,
                                                     numero=numero, larghezza=larghezza, altezza=altezza,
                                                     profondita=profondita)

    def eliminaLavorazione(numero_preventivo, data, ordine):

        toDel = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                          ordine=ordine).first()

        # essendoci il vincolo d'integrita', eliminando una lavorazione si eliminano anche le relative sottolavorazioni
        PreventivoFiniture.delRow(toDel)

    def eliminaSottoprodotto(numero_preventivo, data, ordine, ordine_sottoprodotto):

        unitaMisura = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                ordine=ordine).first().unitaMisura
        toDel = None

        if unitaMisura == 'cad':
            toDel = __ProdottoCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine,
                                                                      ordine_sottolavorazione=ordine_sottoprodotto).first()
        elif unitaMisura == 'ml':
            toDel = __ProdottoMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                     ordine=ordine,
                                                                     ordine_sottolavorazione=ordine_sottoprodotto).first()

        elif unitaMisura == 'mq':
            toDel = __ProdottoMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                     ordine=ordine,
                                                                     ordine_sottolavorazione=ordine_sottoprodotto).first()

        elif unitaMisura == 'mc':
            toDel = __ProdottoMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                     ordine=ordine,
                                                                     ordine_sottolavorazione=ordine_sottoprodotto).first()

        PreventivoFiniture.delRow(toDel)

    def __settaOrdineNegativo__(lavorazione, queryClass):

        newOrdine = int(-lavorazione.ordine)

        queryClass.filter_by(numero_preventivo=lavorazione.numero_preventivo, data=lavorazione.data,
                             ordine=lavorazione.ordine).update({'ordine': newOrdine})

    def iniziaRiordinoLavorazione(numero_preventivo, data):
        '''
           Prima di ogni riordino di voci all'interno del preventivo si prendono tutte le voci
           e si setta il loro campo "ordine" al negativo. Questo previene la situazione
           in cui cambiando il numero d'ordine di una voce ci si ritrovi in una situazione intermedia
           con due voci con lo stesso numero ( situazione d'errore in quanto ordine e' parte della chiave
           di una lavorazione) e, allo stesso tempo, di ricordare il vecchio ordine.
        '''

        prodPrev = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).all()
        iniziaNuovoRiordino = True

        '''
        se son gia' presenti dei campi "ordine" negativi, vuol dire che e' gia' in atto un riordino
        e quindi non va chiamata __settaOrdineNegativo__()
        '''
        for prod in prodPrev:
            if prod.ordine < 0:
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            for prod in prodPrev:
                # per ogni lavorazione risetta automaticamente anche le relative sottorelazioni
                # a causa del vincolo d'integrita'
                PreventivoFiniture.__settaOrdineNegativo__(prod, __ProdottiPreventivo__.query)

            PreventivoFinitureDBmodel.commit()

    def modificaOrdineProdotto(modifica, numero_preventivo, data, ordine):

        __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                  ordine=ordine).update(modifica)

        PreventivoFinitureDBmodel.commit()

    def modificaProdotto(modifica, numero_preventivo, data, ordine):

        __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                  ordine=ordine).update(modifica)

        PreventivoFinitureDBmodel.commit()

    def __settaOrdineSottoprodottoNegativo__(sottoprodotto, queryClass):
        newOrdine = int(-sottoprodotto.ordine_sottolavorazione)

        queryClass.filter_by(numero_preventivo=sottoprodotto.numero_preventivo, data=sottoprodotto.data,
                             ordine=sottoprodotto.ordine,
                             ordine_sottolavorazione=sottoprodotto.ordine_sottoprodotto).update(
            {'ordine_sottoprodotto': newOrdine})

    def iniziaRiordinoSottoprodotto(numero_preventivo, data, ordine, unitaMisura):
        '''
        La logica seguita da questa funzione è la stessa di iniziaRiordinoProdotto()
        '''
        queryClassSottoprodotto = None

        if unitaMisura == 'cad':
            queryClassSottoprodotto = __ProdottoCadPreventivo__.query

        elif unitaMisura == 'ml':
            queryClassSottoprodotto = __ProdottoMlPreventivo__.query

        elif unitaMisura == 'mq':
            queryClassSottoprodotto = __ProdottoMqPreventivo__.query

        elif unitaMisura == 'mc':
            queryClassSottoprodotto = __ProdottoMcPreventivo__.query

        sottoprodPrev = queryClassSottoprodotto.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                            ordine=ordine).all()
        iniziaNuovoRiordino = True

        '''
        se son gia' presenti dei campi "ordine" negativi, vuol dire che e' gia' in atto un riordino
        e quindi non va chiamata __settaOrdineSottoprodottoNegativo__()
        '''
        for prod in sottoprodPrev:
            if prod.ordine_sottolavorazione < 0:
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            for prod in sottoprodPrev:
                PreventivoFiniture.__settaOrdineSottoprodottoNegativo__(prod, queryClassSottoprodotto)

            PreventivoFinitureDBmodel.commit()


    def modificaOrdineSottoprodotto(numero_preventivo, data, ordine, old_ordine_sottoprodotto, unitaMisura,
                                       new_ordine_sottoprodotto):

        if unitaMisura == 'cad':
            __ProdottoCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                              ordine=ordine,
                                                              ordine_sottolavorazione=old_ordine_sottoprodotto).update(
                {'ordine_sottolavorazione': new_ordine_sottoprodotto})
        elif unitaMisura == 'ml':
            __ProdottoMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottoprodotto).update(
                {'ordine_sottolavorazione': new_ordine_sottoprodotto})

        elif unitaMisura == 'mq':
            __ProdottoMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottoprodotto).update(
                {'ordine_sottolavorazione': new_ordine_sottoprodotto})

        elif unitaMisura == 'mc':
            __ProdottoMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottoprodotto).update(
                {'ordine_sottolavorazione': new_ordine_sottoprodotto})

        PreventivoFinitureDBmodel.commit()

    def modificaSottoprodotto(modifica, numero_preventivo, data, ordine, ordine_sottoprodotto, unitaMisura):

        if unitaMisura == 'cad':
            __ProdottoCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                              ordine=ordine,
                                                              ordine_sottolavorazione=ordine_sottoprodotto).update(
                modifica)
        elif unitaMisura == 'ml':
            __ProdottoMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=ordine_sottoprodotto).update(
                modifica)

        elif unitaMisura == 'mq':
            __ProdottoMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=ordine_sottoprodotto).update(
                modifica)

        elif unitaMisura == 'mc':
            __ProdottoMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=ordine_sottoprodotto).update(
                modifica)

        PreventivoFinitureDBmodel.commit()

    def returnSinglePreventivo(numero_preventivo, data):

        '''

        :param: la chiave di un preventivo
        :return: una coppia dalla forma: ( ordineSettori, resultLav )
            dove:
            - ordineSettori = lista ordinata di nomi di settore; ogni elemento appare una sola volta
                                e l'ordine riflette quello di comparsa nel relativo preventivo;
            - resultLav = lista di tuple; ogni tupla racchiude tutta l'informazione utile su una specifica
                            lavorazione nel preventivo.

            L'ordine di ogni tupla elemento di resultLav riflette quello di comparsa nel relativo preventivo;

            Ogni tupla elemento di resultLav ha la forma: (lavorazione, quantita, totale, sottolavorazioni).
        '''

        prodotti = __ProdottiPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).order_by(
                                                                __ProdottiPreventivo__.ordine).all()

        ordineTipologia = []
        resultProd = []

        for prod in prodotti:
            sottoprodotti = []

            if not ordineTipologia.__contains__(prod.settore):
                ordineTipologia.append(prod.settore)

            if prod.unitaMisura == 'cad':

                sottoprodotti = __ProdottoCadPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=prod.ordine).order_by(
                                        __ProdottoCadPreventivo__.ordine_sottoprodotto).all()
                quantitaTotale = 0

                for sottolav in sottoprodotti:
                    quantitaTotale += sottolav.numero

                prezzoTotale = quantitaTotale * prod.prezzoUnitario

                resultProd.append((prod, quantitaTotale, prezzoTotale, sottoprodotti))

            elif prod.unitaMisura == 'ml':
                sottoprodotti = __ProdottoMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=prod.ordine).order_by(
                                        __ProdottoMlPreventivo__.ordine_sottoprodotto).all()

                quantitaTotale = 0

                for sottolav in sottoprodotti:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)

                prezzoTotale = quantitaTotale * prod.prezzoUnitario

                resultProd.append((prod, quantitaTotale, prezzoTotale, sottoprodotti))


            elif prod.unitaMisura == 'mq':
                sottoprodotti = __ProdottoMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=prod.ordine).order_by(
                                        __ProdottoMqPreventivo__.ordine_sottoprodotto).all()

                quantitaTotale = 0

                for sottolav in sottoprodotti:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)

                prezzoTotale = quantitaTotale * prod.prezzoUnitario

                resultProd.append((prod, quantitaTotale, prezzoTotale, sottoprodotti))



            elif prod.unitaMisura == 'mc':
                sottoprodotti = __ProdottoMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=prod.ordine).order_by(
                                        __ProdottoMcPreventivo__.ordine_sottoprodotto).all()

                quantitaTotale = 0

                for sottolav in sottoprodotti:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)

                prezzoTotale = quantitaTotale * prod.prezzoUnitario

                resultProd.append((prod, quantitaTotale, prezzoTotale, sottoprodotti))

        return ( ordineTipologia, resultProd)

    def returnLastPreventivoCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        last_prev = PreventivoFiniture.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                    indirizzo_cliente=indirizzo_cliente).order_by(
            desc(PreventivoFiniture.data), desc(PreventivoFiniture.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoFiniture.returnSinglePreventivo(numero_preventivo=last_prev.numero_preventivo,
                                                                data=last_prev.data)

        return (last_prev,) + preventivoInfo

    def returnAllPreventiviCliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        '''

        :param cognome_cliente:
        :param indirizzo_cliente:
        :return: Ritorna una lista di tutti i preventivi associati ad un dato cliente;
                 in particolare si tratta di una lista di tuple ( di preciso coppie )
                 così formate: ( preventivo, [lavorazioni] ),
                 dove preventivo
                 e' il risultato di una query e [lavorazioni] e' il risultato della
                 chiamata a PreventivoFiniture.returnSinglePreventivo()
        '''

        preventivi = PreventivoFiniture.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(
            PreventivoFiniture.numero_preventivo, desc(PreventivoFiniture.data)).all()

        returnList = []

        for prev in preventivi:
            returnList.append((prev, PreventivoFiniture.returnSinglePreventivo(numero_preventivo=prev.numero_preventivo,
                                                                            data=prev.data)))

        return returnList

    def get_counter_preventivi_per_cliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        q = PreventivoFiniture.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                            indirizzo_cliente=indirizzo_cliente)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def get_counter_preventivi_per_numero(numero_preventivo):
        q = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def stampaPreventivo(numero_preventivo, data):

        preventivo = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, data=data).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        infoPreventivo = PreventivoFiniture.returnSinglePreventivo(numero_preventivo=numero_preventivo, data=data)

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        latexScript = '''    
                        \\documentclass[pdftex,11pt,a4paper]{article} 
                        \\usepackage{graphicx}
                        \\graphicspath{ {./Immagini/} }

                        \\usepackage[legalpaper]{geometry}
                        \\usepackage{eurosym}
                        \\usepackage{xcolor}
                        \\geometry{
                        a4paper,
                        left=30mm,
                        right=30mm,
                        top=10mm,
                        }

                        \\usepackage{fancyhdr}
                        \\pagestyle{fancy}
                        \\fancyfoot[C]{UnionService Srl. Via Roma n. 84 - 37060 Castel d'Azzano (VR) - Tel. +39 045 8521697 - Fax +39 045 8545123 \\\\
                                      Cell. +39 342 7663538 - C.F./P.iva 04240420234 - REA: VR-404097 \\\\\\thepage }

                        \\renewcommand{\\headrulewidth}{0pt}
                        \\renewcommand{\\footrulewidth}{1pt}

                        \\begin{document}
                        \\begin{figure}[!t]
                        \\includegraphics[width=\\textwidth]{intestazioneAlta.jpg}
                        \\end{figure}

                        \\begin{center}
                        \\begin{tabular}{ l  l }
                    '''

        latexScript += 'Nominativo: & {} {} \\\\'.format(cliente.nome, cliente.cognome)
        latexScript += 'Indirizzo: &  {}  \\\\'.format(cliente.indirizzo)
        latexScript += 'Telefono: &  {} \\\\'.format(cliente.telefono)

        latexScript += ' Tipologia commessa: & {} \\\\'.format(preventivo.tipologia_commessa)
        latexScript += '''         
                        \\end{tabular}
                        \\end{center}

                      '''
        latexScript += '''
                        \\vspace{5mm}
                        \\begin{center}
                        \\begin{tabular}{| p{1cm} | p{5cm} | l | l |}
                        \\hline
                        \\textbf{Pos.} & \\textbf{Descrizione} & \\textbf{Quantit\\'a}  & \\textbf{Prezzo Totale} \\\\ 
                       '''
        totale = 0

        for settore in infoPreventivo[0]:
            latexScript += '\\hline'
            latexScript += '& {} & & \\\\ \\hline'.format(settore)

            for lav in infoPreventivo[1]:
                if lav[0].settore == settore:
                    latexScript += '{} & {} & {} {} & \\euro  {} \\\\'.format(lav[0].ordine,
                                                                              lav[0].tipologia_lavorazione, lav[1],
                                                                              lav[0].unitaMisura, lav[2])
                    totale += float(lav[2])

        latexScript += '\\hline'
        latexScript += ' & & & Totale: \\euro {} \\\\'.format(totale)
        latexScript += '''
                        \\hline
                        \\end{tabular}
                        \\end{center}
                       '''

        latexScript += '''
                        \\vspace{20mm}
                        \\textbf{Dalla seguente offera sono escluse:}
                        \\begin{itemize}
                            \\item IVA e qualsiasi altro onere fiscale;
                            \\item Ore in economia per opere extra-capitolato (\\euro/h 23,00);
                            \\item Costi di energia elettrica e acqua ad uso cantiere;
                            \\item Qualsiasi altra voce non citata;
                            \\item Sul totale preventivato ci si riserva di un errore del 5\\% come imprevisti cantiere;
                            \\item Pratica per detrazioni fiscali da quantificare;
                        \\end{itemize}
                        \\
                        \\textbf{Pagamenti}
                        \\begin{itemize}
                            \\item Da concordare in fase di accetazione.
                        \\end{itemize}
                        \\
                        \\textcolor{red}{La presente offerta ha validit\\'a 30 giorni dalla data odierna.}\\\\
                        \\\\
                        \\textbf{Data:} \\hfill  \\textbf{FIRMA per ACCETTAZIONE:} \\\\
                        '''

        latexScript += '{}\\'.format(oggi)

        latexScript += '''
                        \\end{document}
                       '''

        with open('app/preventiviLatexDir/preventivo.tex', mode='w') as prova:
            prova.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex preventivo.tex")