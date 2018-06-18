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

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, tipologia_commessa, dipendente_ultimaModifica=None):

        self.numero_preventivo=numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.tipologia_commessa=tipologia_commessa

        if dipendente_ultimaModifica is None:
            self.dipendente_ultimaModifica = dipendente_generatore
        else:
            self.dipendente_ultimaModifica = dipendente_ultimaModifica

    def calcolaCodicePreventivo(self):
        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo)+dipendente+str(annoPreventivo)


    def registraPreventivo( nome_cliente, cognome_cliente, indirizzo_cliente ,
                            dipendente_generatore, tipologia_commessa):

        youngerPrev = PreventivoEdile.query.order_by(desc(PreventivoEdile.numero_preventivo)).first()
        lastNumPrev=99

        #se ci sono gia' preventivi registrati prende il numero_preventivo del piu' recente
        if youngerPrev is not None:
            lastNumPrev=youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoEdile(numero_preventivo=lastNumPrev+1, data=oggi, nome_cliente=nome_cliente,
                                     cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore, tipologia_commessa=tipologia_commessa)

        PreventivoEdileDBmodel.addRow(preventivo)

        return ( lastNumPrev+1, oggi )


    def modificaPreventivo(numero_preventivo, dipendente_ultimaModifica):
        '''
         Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
         piu' recente, ne fa una copia ( compresa di lavorazioni e sottolavorazioni ) cambiando unicamente
         gli attributi "data", settata alla data odierna, e "dipendente_ultimaModifica", settato con lo username
         del dipendente che sta facendo la modifica.

        :param numero_preventivo, dipendente_ultimaModifica:
        :return:
        '''

        lastPrev = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo).order_by(PreventivoEdile.data).first()
        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        #se il preventivo viene modificato piu' volte lo stesso giorno o viene modificato
        # il giorno non viene fatta alcuna copia e viene unicamente modificato
        # il parametro "dipendente_ultimaModifica"

        if now ==lastPrev.data:
            PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo).update(
                        {'dipendente_ultimaModifica' : dipendente_ultimaModifica})

            PreventivoEdile.commit()

            return (numero_preventivo, oggi)

        preventivo = PreventivoEdile(numero_preventivo=lastPrev.numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=lastPrev.dipendente_generatore,
                                     tipologia_commessa=lastPrev.tipologia_commessa,
                                     dipendente_ultimaModifica=dipendente_ultimaModifica)

        PreventivoEdileDBmodel.addRow(preventivo)

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        for lav in lavorazioni:
            lav.data = oggi

        PreventivoEdileDBmodel.addRow(lavorazioni)

        sottolavorazioniCad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMl = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()


        sottolavorazioni = sottolavorazioniCad + sottolavorazioniMl + sottolavorazioniMc + sottolavorazioniMq

        for sottoLav in sottolavorazioni:
            sottoLav.data= oggi

        PreventivoEdileDBmodel.addRow(sottolavorazioni)


        return ( numero_preventivo, oggi )


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


    def nuovaSottolavorazione(numero_preventivo, data, ordine):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first().unitaMisura


        if unitaMisura == 'cad':
            last_sottolav_cad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                  data=data, ordine=ordine).order_by( desc(__SottolavorazioneCadPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                             ordine=ordine, ordine_sottolavorazione=last_sottolav_cad+1, numero=1 )
        elif unitaMisura == 'ml':
            last_sottolav_ml = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMlPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_ml+1,
                                                         numero=1, larghezza=1)

        elif unitaMisura == 'mq':
            last_sottolav_mq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMqPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mq+1,
                                                         numero=1, larghezza=1, altezza=1)


        elif unitaMisura == 'mc':
            last_sottolav_mc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMcPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mc+1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1)



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

        lavPrev = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).all()
        iniziaNuovoRiordino = True

        '''
        se son gia' presenti dei campi "ordine" negativi, vuol dire che e' gia' in atto un riordino
        e quindi non va chiamata __settaOrdineNegativo__()
        '''
        for lav in lavPrev:
            if lav.ordine < 0 :
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            for lav in lavPrev:
                # per ogni lavorazione risetta automaticamente anche le relative sottorelazioni
                # a causa del vincolo d'integrita'
                PreventivoEdile.__settaOrdineNegativo__(lav, __LavorazionePreventivo__.query)

            PreventivoEdileDBmodel.commit()


    def modificaOrdineLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoEdileDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoEdileDBmodel.commit()

    def __settaOrdineSottolavorazioneNegativo__(sottolavorazione, queryClass):
        app.server.logger.info("sTo siordinando la sottolav nun: {}".format(sottolavorazione.ordine_sottolavorazione) )
        newOrdine = int(-sottolavorazione.ordine_sottolavorazione)

        queryClass.filter_by(numero_preventivo=sottolavorazione.numero_preventivo, data=sottolavorazione.data,
                             ordine=sottolavorazione.ordine,
                             ordine_sottolavorazione=sottolavorazione.ordine_sottolavorazione).update({'ordine_sottolavorazione': newOrdine})

    def iniziaRiordinoSottolavorazione(numero_preventivo, data, ordine, unitaMisura):
        '''
        La logica seguita da questa funzione è la stessa di iniziaRiordinoLavorazione()
        '''
        queryClassSottolavorazione = None

        if unitaMisura == 'cad':
            queryClassSottolavorazione = __SottolavorazioneCadPreventivo__.query

        elif unitaMisura == 'ml':
            queryClassSottolavorazione = __SottolavorazioneMlPreventivo__.query

        elif unitaMisura == 'mq':
            queryClassSottolavorazione = __SottolavorazioneMqPreventivo__.query

        elif unitaMisura == 'mc':
            queryClassSottolavorazione = __SottolavorazioneMcPreventivo__.query

        sottolavPrev = queryClassSottolavorazione.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).all()
        iniziaNuovoRiordino = True

        '''
        se son gia' presenti dei campi "ordine" negativi, vuol dire che e' gia' in atto un riordino
        e quindi non va chiamata __settaOrdineSottolavorazioneNegativo__()
        '''
        for lav in sottolavPrev:
            if lav.ordine_sottolavorazione < 0 :
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            app.server.logger.info("\n\nEntrato in Inizio riordino {} {}\n\n".format(ordine, unitaMisura))
            for lav in sottolavPrev:
                PreventivoEdile.__settaOrdineSottolavorazioneNegativo__(lav, queryClassSottolavorazione)

            PreventivoEdileDBmodel.commit()

        app.server.logger.info('fine rinumerazione')


    def modificaOrdineSottolavorazione(numero_preventivo, data, ordine, old_ordine_sottolavorazione, unitaMisura,
                                       new_ordine_sottolavorazione):


        app.server.logger.info('\n\nInizio modifica ordine {}\n\n'.format(unitaMisura))
        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                              ordine=ordine,
                                                              ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                { 'ordine_sottolavorazione': new_ordine_sottolavorazione })
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        PreventivoEdileDBmodel.commit()
    def modificaSottolavorazione(modifica, numero_preventivo, data, ordine, ordine_sottolavorazione, unitaMisura):

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

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).order_by(
                                                                __LavorazionePreventivo__.ordine).all()

        ordineSettori = []
        resultLav = []

        for lav in lavorazioni:
            sottolavorazioni = []

            if not ordineSettori.__contains__(lav.settore):
                ordineSettori.append(lav.settore)

            if lav.unitaMisura == 'cad':

                sottolavorazioni = __SottolavorazioneCadPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneCadPreventivo__.ordine_sottolavorazione).all()
                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += sottolav.numero

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'ml':
                sottolavorazioni = __SottolavorazioneMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMlPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


            elif lav.unitaMisura == 'mq':
                sottolavorazioni = __SottolavorazioneMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMqPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))



            elif lav.unitaMisura == 'mc':
                sottolavorazioni = __SottolavorazioneMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

        return ( ordineSettori, resultLav)

    def returnLastPreventivoCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        last_prev = PreventivoEdile.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(desc(PreventivoEdile.data), desc(PreventivoEdile.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=last_prev.numero_preventivo, data=last_prev.data)


        return ( last_prev, ) + preventivoInfo

    def returnAllPreventiviCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        preventivi = PreventivoEdile.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(desc(PreventivoEdile.data)).all()

        return preventivi


