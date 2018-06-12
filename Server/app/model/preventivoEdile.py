from .db.preventivoEdileDBmodel import PreventivoEdileDBmodel
from .db.lavorazioniPreventivoEdile.lavorazionePreventivoDBmodel import LavorazionePreventivoDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneCadDBmodel import SottolavorazioneCadDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMlDBmodel import SottolavorazioneMlDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMqDBmodel import SottolavorazioneMqDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMcDBmodel import SottolavorazioneMcDBmodel
from sqlalchemy import desc
import datetime
import app

class __SottolavorazioneCadPreventivo__(SottolavorazioneCadDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione

        self.numero = numero


class __SottolavorazioneMlPreventivo__(SottolavorazioneMlDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione

        self.numero = numero
        self.larghezza = larghezza



class __SottolavorazioneMqPreventivo__(SottolavorazioneMqDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza



class __SottolavorazioneMcPreventivo__(SottolavorazioneMcDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza, profondita ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita


class __LavorazionePreventivo__(LavorazionePreventivoDBmodel):
    def __init__(self,  numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine

        self.settore = settore
        self.tipologia_lavorazione = tipologia_lavorazione
        self.unitaMisura=unitaMisura
        self.prezzoUnitario=prezzoUnitario

class PreventivoEdile(PreventivoEdileDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente, indirizzo_cliente):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente



    def registraPreventivo( nome_cliente, cognome_cliente, indirizzo_cliente ):

        youngerPrev = PreventivoEdile.query.order_by(desc(PreventivoEdile.numero_preventivo)).first()
        lastNumPrev=0

        if youngerPrev is not None:
            lastNumPrev=youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoEdile(numero_preventivo=lastNumPrev+1, data=oggi, nome_cliente=nome_cliente,
                                        cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente)

        PreventivoEdileDBmodel.addRow(preventivo)

        return ( lastNumPrev+1, oggi )



    def __calcolcaOrdineSottolavorazione__( queryClass, numero_preventivo, data, ordine):
        ordine_sottolavorazione = 0

        aux = queryClass.filter_by(numero_preventivo=numero_preventivo, data=data,
                                   ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        while aux is not None:
            ordine_sottolavorazione += 1
            aux = queryClass.filter_by(numero_preventivo=numero_preventivo, data=data,
                                       ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        return ordine_sottolavorazione

    def __registraSottolavorazione__( numero_preventivo, data, ordine, ordine_sottolavorazione, unitaMisura,
                                        numero,  larghezza=None, altezza=None, profondita=None):

        lavorazione = None
        if unitaMisura == 'cad':
            lavorazione = __SottolavorazioneCadPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione, numero=numero )
        elif unitaMisura == 'ml':
            lavorazione = __SottolavorazioneMlPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza )

        elif unitaMisura == 'mq':
            lavorazione = __SottolavorazioneMqPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza )

        elif unitaMisura == 'mc':
            lavorazione = __SottolavorazioneMcPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita)

        PreventivoEdileDBmodel.addRow(lavorazione)


    def registraLavorazione( numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario,
                             numero, larghezza=None, altezza=None, profondita=None ):

        controlVar = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:
            lavorazione = __LavorazionePreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                    ordine=ordine, settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                                    unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario)
            PreventivoEdileDBmodel.addRow(lavorazione)
        else: # se la lavorazione e' gia' presente registra la sottolavorazione

            if unitaMisura == 'cad':
                ordineSottolavorazione=PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneCadPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)
            elif unitaMisura == 'ml':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMlPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

            elif unitaMisura == 'mq':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMqPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

            elif unitaMisura == 'mc':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMcPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

        PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                     ordine=ordine, ordine_sottolavorazione=ordineSottolavorazione,
                                                     numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita)


    def eliminaLavorazione(numero_preventivo, data, ordine ):

        toDel = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()

        # essendoci il vincolo d'integrita', eliminando una lavorazione si eliminano anche le relative sottolavorazioni
        PreventivoEdile.delRow(toDel)


    def eliminaSottolavorazione(numero_preventivo, data, ordine, ordine_sottolavorazione):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                          ordine=ordine).first().unitaMisura
        toDel = None

        if unitaMisura == 'cad':
            toDel = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()
        elif unitaMisura == 'ml':
            toDel = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mq':
            toDel = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mc':
            toDel = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()


        PreventivoEdile.delRow(toDel)



    def __settaOrdineNegativo__(lavorazione, queryClass):

        prov = queryClass.filter_by(numero_preventivo=lavorazione.numero_preventivo, data=lavorazione.data, ordine=lavorazione.ordine).first()
        app.server.logger.info("\n\n\nInizio ordine negativoa {}\n\n\n".format(prov))

        newOrdine = int(-lavorazione.ordine)

        queryClass.filter_by(numero_preventivo=lavorazione.numero_preventivo, data=lavorazione.data,
                                           ordine=lavorazione.ordine).update({'ordine': newOrdine})

        PreventivoEdileDBmodel.commit()

        app.server.logger.info("\n\n\nfine ordine negativo\n\n\n")

    def inziaRiordinoLavorazione(numero_preventivo, data):
        '''
           Prima di ogni riordino di voci all'interno del preventivo si prendono tutte le voci
           e si setta il loro campo "ordine" al negativo. Questo previene la situazione
           in cui cambiando il numero d'ordine di una voce ci si ritrovi in una situazione intermedia
           con due voci con lo stesso numero ( situazione d'errore in quanto ordine e' parte della chiave
           di una lavorazione) e, allo stesso tempo, di ricordare il vecchio ordine.
        '''

        app.server.logger.info("\n\n\nInizio riordino \n\n\n")

        lavPrev = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).all()
        iniziaNuovoRiordino = True

        '''
        se son gia' presenti dei campi "ordine" negativi, vuol dire che e' gia' in atto un riordino
        e quindi non va chiamata __settaOrdineNegativo__()
        '''
        for lav in lavPrev:
            if lav.ordine < 0 :
                iniziaNuovoRiordino = False

        app.server.logger.info("\n\n\nIVariabile inizia nuovo riordino e' {}\n\n\n".format(iniziaNuovoRiordino))
        if iniziaNuovoRiordino:
            for lav in lavPrev:
                app.server.logger.info("\n\n\nl'ordine della lavorazione e' {}\n\n\n".format(lav.ordine))
                # per ogni lavorazione risetta automaticamente anche le relative sottorelazioni
                # a causa del vincolo d'integrita'
                PreventivoEdile.__settaOrdineNegativo__(lav, __LavorazionePreventivo__.query)




    def modificaOrdineLavorazione( modifica, numero_preventivo, data, ordine):
        app.server.logger.info("\n\n\nInizio a modificare l'ordine di lavorazione " +str(ordine))


        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoEdileDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoEdileDBmodel.commit()

    def modificaSottolavorazione(modifica, numero_preventivo, data, ordine, ordine_sottolavorazione):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first().unitaMisura

        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione ).update(modifica)
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        PreventivoEdileDBmodel.commit()