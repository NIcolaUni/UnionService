from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.lavorazioniPreventivoVarianti.lavorazionePreventivoVariantiDBmodel import LavorazionePreventivoVariantiDBmodel
from .db.lavorazioniPreventivoVarianti.sottolavorazioni.sottolavorazioneVariantiCadDBmodel import SottolavorazioneVariantiCadDBmodel
from .db.lavorazioniPreventivoVarianti.sottolavorazioni.sottolavorazioneVariantiMlDBmodel import SottolavorazioneVariantiMlDBmodel
from .db.lavorazioniPreventivoVarianti.sottolavorazioni.sottolavorazioneVariantiMqDBmodel import SottolavorazioneVariantiMqDBmodel
from .db.lavorazioniPreventivoVarianti.sottolavorazioni.sottolavorazioneVariantiMcDBmodel import SottolavorazioneVariantiMcDBmodel
from .clienteAccolto import  ClienteAccolto
from .dipendente import Dipendente
from sqlalchemy import desc, func
import datetime
import app
import os
import math

class __SottolavorazioneVariantiCadPreventivo__(SottolavorazioneVariantiCadDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'varianti'

        self.numero = numero


class __SottolavorazioneVariantiMlPreventivo__(SottolavorazioneVariantiMlDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'varianti'

        self.numero = numero
        self.larghezza = larghezza



class __SottolavorazioneVariantiMqPreventivo__(SottolavorazioneVariantiMqDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'varianti'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza



class __SottolavorazioneVariantiMcPreventivo__(SottolavorazioneVariantiMcDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza, profondita ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'varianti'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita


class __LavorazionePreventivoVarianti__(LavorazionePreventivoVariantiDBmodel):
    def __init__(self,  numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.tipologia = 'varianti'

        self.settore = settore
        self.tipologia_lavorazione = tipologia_lavorazione
        self.unitaMisura=unitaMisura
        self.prezzoUnitario=prezzoUnitario


class __Commessa__(CommessaDBmodel):
    def __init__(self, numero_preventivo, intervento, indirizzo, comune):
        self.numero_preventivo = numero_preventivo
        self.intervento = intervento
        self.indirizzo = indirizzo
        self.comune = comune

class PreventivoVarianti(PreventivoDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, intervento_commessa,
                 indirizzo_commessa, comune_commessa, stato=True):

        oldCommessa = __Commessa__.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=intervento_commessa).first()

        if oldCommessa is None:
            commessa = __Commessa__(numero_preventivo=numero_preventivo, intervento=intervento_commessa,
                                    indirizzo=indirizzo_commessa, comune=comune_commessa)
            __Commessa__.addRow(commessa)

        self.numero_preventivo=numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.intervento_commessa=intervento_commessa
        self.tipologia = 'varianti'
        self.stato = stato


    def calcolaCodicePreventivo(self):
        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo)+dipendente+str(annoPreventivo)

    def calcolaCodicePreventivoNoObj(numero_preventivo, data):

        prev = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='varianti').first()

        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = prev.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = prev.dipendente_generatore.split('_')[1][0:3].upper()

        return str(prev.numero_preventivo)+dipendente+str(annoPreventivo)

    def registraPreventivo( dipendente_generatore, numero_preventivo ):


        oldPrev = PreventivoVarianti.query.filter_by(numero_preventivo=numero_preventivo,
                                                     tipologia='varianti').order_by(desc(PreventivoVarianti.data)).first()

        if oldPrev is not None:
            return PreventivoVarianti.modificaPreventivo(numero_preventivo=numero_preventivo, data=oldPrev.data,
                                                  dipendente_generatore=dipendente_generatore)

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)



        prevEdile = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, tipologia='edile').first()

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=prevEdile.intervento_commessa).first()

        preventivo = PreventivoVarianti(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=prevEdile.nome_cliente,
                                     cognome_cliente=prevEdile.cognome_cliente, indirizzo_cliente=prevEdile.indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=commessa.intervento,
                                     indirizzo_commessa=commessa.indirizzo, comune_commessa=commessa.comune)

        PreventivoDBmodel.addRow(preventivo)

        return ( numero_preventivo, oggi )

    def eliminaPreventivo(numero_preventivo, data):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data).first()

        PreventivoDBmodel.delRow(toDel)

    def __duplicaSottolavorazioni__(sottolavorazioni, unitaMisura):

        returnList = []

        if unitaMisura == 'cad':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneVariantiCadPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                                data=sottolav.data, ordine=sottolav.ordine,
                                                                ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                                numero=sottolav.numero)
                returnList.append(newSottolav)

        elif unitaMisura == 'ml':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneVariantiMlPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza)
                returnList.append(newSottolav)

        elif unitaMisura == 'mq':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneVariantiMqPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza)
                returnList.append(newSottolav)

        elif unitaMisura == 'mc':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneVariantiMcPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, profondita=sottolav.profondita)
                returnList.append(newSottolav)

        return returnList

    def __duplicaLavorazioni__(lavorazioni):

        app.server.logger.info("\n\nEntrato in duplica lav\n")

        returnList = []
        for lav in lavorazioni:
            newLav = __LavorazionePreventivoVarianti__(numero_preventivo=lav.numero_preventivo, data=lav.data,
                                               ordine=lav.ordine,
                                               settore=lav.settore, tipologia_lavorazione=lav.tipologia_lavorazione,
                                               unitaMisura=lav.unitaMisura, prezzoUnitario=lav.prezzoUnitario)
            returnList.append(newLav)

        return returnList

    def modificaPreventivo(numero_preventivo, data, dipendente_generatore):
        '''
         Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
         piu' recente, ne fa una copia ( compresa di lavorazioni e sottolavorazioni ) cambiando unicamente
         gli attributi "data", settata alla data odierna, e "dipendente_ultimaModifica", settato con lo username
         del dipendente che sta facendo la modifica.

        :param numero_preventivo, dipendente_ultimaModifica:
        :return:
        '''

        lastPrev = PreventivoVarianti.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='varianti').first()
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        #se il preventivo viene modificato piu' volte lo stesso giorno o viene modificato
        # il giorno non viene fatta alcuna copia"

        if str(now).split(' ')[0] == str(lastPrev.data):
            return (numero_preventivo, oggi)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=lastPrev.intervento_commessa).first()

        preventivo = PreventivoVarianti(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=commessa.intervento,
                                     indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune)


        PreventivoDBmodel.addRow(preventivo)

        lavorazioni = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        lavorazioni = PreventivoVarianti.__duplicaLavorazioni__(lavorazioni)

        for lav in lavorazioni:
            lav.data = oggi
            PreventivoDBmodel.addRowNoCommit(lav)

        PreventivoVarianti.commit()

        sottolavorazioniCad = __SottolavorazioneVariantiCadPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniCad = PreventivoVarianti.__duplicaSottolavorazioni__(sottolavorazioniCad, 'cad')

        sottolavorazioniMl = __SottolavorazioneVariantiMlPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMl = PreventivoVarianti.__duplicaSottolavorazioni__(sottolavorazioniMl, 'ml')

        sottolavorazioniMq = __SottolavorazioneVariantiMqPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMq = PreventivoVarianti.__duplicaSottolavorazioni__(sottolavorazioniMq, 'mq')

        sottolavorazioniMc = __SottolavorazioneVariantiMcPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMc = PreventivoVarianti.__duplicaSottolavorazioni__(sottolavorazioniMc, 'mc')

        sottolavorazioni = sottolavorazioniCad + sottolavorazioniMl + sottolavorazioniMc + sottolavorazioniMq

        for sottoLav in sottolavorazioni:
            sottoLav.data= oggi
            PreventivoDBmodel.addRowNoCommit(sottoLav)

        PreventivoVarianti.commit()

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
            lavorazione = __SottolavorazioneVariantiCadPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione, numero=numero )
        elif unitaMisura == 'ml':
            lavorazione = __SottolavorazioneVariantiMlPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza )

        elif unitaMisura == 'mq':
            lavorazione = __SottolavorazioneVariantiMqPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza )

        elif unitaMisura == 'mc':
            lavorazione = __SottolavorazioneVariantiMcPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita)

        PreventivoDBmodel.addRow(lavorazione)


    def nuovaSottolavorazione(numero_preventivo, data, ordine):

        unitaMisura = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first().unitaMisura


        if unitaMisura == 'cad':
            last_sottolav_cad = __SottolavorazioneVariantiCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                  data=data, ordine=ordine).order_by( desc(__SottolavorazioneVariantiCadPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoVarianti.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                             ordine=ordine, ordine_sottolavorazione=last_sottolav_cad+1, numero=1 )
        elif unitaMisura == 'ml':
            last_sottolav_ml = __SottolavorazioneVariantiMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneVariantiMlPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoVarianti.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_ml+1,
                                                         numero=1, larghezza=1)

        elif unitaMisura == 'mq':
            last_sottolav_mq = __SottolavorazioneVariantiMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneVariantiMqPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoVarianti.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mq+1,
                                                         numero=1, larghezza=1, altezza=1)


        elif unitaMisura == 'mc':
            last_sottolav_mc = __SottolavorazioneVariantiMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneVariantiMcPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoVarianti.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mc+1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1)



    def registraLavorazione( numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario,
                             numero, larghezza=None, altezza=None, profondita=None ):

        controlVar = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:
            lavorazione = __LavorazionePreventivoVarianti__(numero_preventivo=numero_preventivo, data=data,
                                                    ordine=ordine, settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                                    unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario)
            PreventivoDBmodel.addRow(lavorazione)
        else: # se la lavorazione e' gia' presente registra la sottolavorazione

            if unitaMisura == 'cad':
                ordineSottolavorazione=PreventivoVarianti.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneVariantiCadPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)
            elif unitaMisura == 'ml':
                ordineSottolavorazione =PreventivoVarianti.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneVariantiMlPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

            elif unitaMisura == 'mq':
                ordineSottolavorazione =PreventivoVarianti.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneVariantiMqPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

            elif unitaMisura == 'mc':
                ordineSottolavorazione =PreventivoVarianti.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneVariantiMcPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, data=data,
                                                                   ordine=ordine)

        PreventivoVarianti.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                     ordine=ordine, ordine_sottolavorazione=ordineSottolavorazione,
                                                     numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita)


    def eliminaLavorazione(numero_preventivo, data, ordine ):

        toDel = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()

        # essendoci il vincolo d'integrita', eliminando una lavorazione si eliminano anche le relative sottolavorazioni
        PreventivoVarianti.delRow(toDel)


    def eliminaSottolavorazione(numero_preventivo, data, ordine, ordine_sottolavorazione):

        unitaMisura = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                          ordine=ordine).first().unitaMisura
        toDel = None

        if unitaMisura == 'cad':
            toDel = __SottolavorazioneVariantiCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()
        elif unitaMisura == 'ml':
            toDel = __SottolavorazioneVariantiMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mq':
            toDel = __SottolavorazioneVariantiMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mc':
            toDel = __SottolavorazioneVariantiMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()


        PreventivoVarianti.delRow(toDel)


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

        lavPrev = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data).all()
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
                PreventivoVarianti.__settaOrdineNegativo__(lav, __LavorazionePreventivoVarianti__.query)

            PreventivoDBmodel.commit()


    def modificaOrdineLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()

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
            queryClassSottolavorazione = __SottolavorazioneVariantiCadPreventivo__.query

        elif unitaMisura == 'ml':
            queryClassSottolavorazione = __SottolavorazioneVariantiMlPreventivo__.query

        elif unitaMisura == 'mq':
            queryClassSottolavorazione = __SottolavorazioneVariantiMqPreventivo__.query

        elif unitaMisura == 'mc':
            queryClassSottolavorazione = __SottolavorazioneVariantiMcPreventivo__.query

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
                PreventivoVarianti.__settaOrdineSottolavorazioneNegativo__(lav, queryClassSottolavorazione)

            PreventivoDBmodel.commit()

        app.server.logger.info('fine rinumerazione')


    def modificaOrdineSottolavorazione(numero_preventivo, data, ordine, old_ordine_sottolavorazione, unitaMisura,
                                       new_ordine_sottolavorazione):


        app.server.logger.info('\n\nInizio modifica ordine {}\n\n'.format(unitaMisura))
        if unitaMisura == 'cad':
            __SottolavorazioneVariantiCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                              ordine=ordine,
                                                              ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                { 'ordine_sottolavorazione': new_ordine_sottolavorazione })
        elif unitaMisura == 'ml':
            __SottolavorazioneVariantiMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mq':
            __SottolavorazioneVariantiMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mc':
            __SottolavorazioneVariantiMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        PreventivoDBmodel.commit()
    def modificaSottolavorazione(modifica, numero_preventivo, data, ordine, ordine_sottolavorazione, unitaMisura):

        if unitaMisura == 'cad':
            __SottolavorazioneVariantiCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione ).update(modifica)
        elif unitaMisura == 'ml':
            __SottolavorazioneVariantiMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mq':
            __SottolavorazioneVariantiMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mc':
            __SottolavorazioneVariantiMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        PreventivoDBmodel.commit()

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

        lavorazioni = __LavorazionePreventivoVarianti__.query.filter_by(numero_preventivo=numero_preventivo, data=data).order_by(
                                                                __LavorazionePreventivoVarianti__.ordine).all()

        ordineSettori = []
        resultLav = []

        for lav in lavorazioni:
            sottolavorazioni = []

            if not ordineSettori.__contains__(lav.settore):
                ordineSettori.append(lav.settore)

            if lav.unitaMisura == 'cad':

                sottolavorazioni = __SottolavorazioneVariantiCadPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneVariantiCadPreventivo__.ordine_sottolavorazione).all()
                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += sottolav.numero

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'ml':
                sottolavorazioni = __SottolavorazioneVariantiMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneVariantiMlPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


            elif lav.unitaMisura == 'mq':
                sottolavorazioni = __SottolavorazioneVariantiMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneVariantiMqPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))



            elif lav.unitaMisura == 'mc':
                sottolavorazioni = __SottolavorazioneVariantiMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneVariantiMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

        return ( ordineSettori, resultLav)

    def returnLastPreventivoCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        last_prev = PreventivoVarianti.query.filter_by(tipologia='varianti', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(desc(PreventivoVarianti.data), desc(PreventivoVarianti.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoVarianti.returnSinglePreventivo(numero_preventivo=last_prev.numero_preventivo, data=last_prev.data)


        return ( last_prev, ) + preventivoInfo

    def returnAllPreventiviCliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        '''

        :param cognome_cliente:
        :param indirizzo_cliente:
        :return: Ritorna una lista di tutti i preventivi associati ad un dato cliente;
                 in particolare si tratta di una lista di tuple ( di preciso coppie )
                 così formate: ( preventivo, [lavorazioni] ),
                 dove preventivo
                 e' il risultato di una query e [lavorazioni] e' il risultato della
                 chiamata a PreventivoVarianti.returnSinglePreventivo()
        '''

        preventivi = PreventivoVarianti.query.filter_by(tipologia='varianti', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(
                                                        PreventivoVarianti.numero_preventivo, desc(PreventivoVarianti.data)).all()

        returnList = []

        for prev in preventivi:
            returnList.append( ( prev, PreventivoVarianti.returnSinglePreventivo(numero_preventivo=prev.numero_preventivo, data=prev.data)) )

        return returnList

    def get_counter_preventivi_per_cliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        q = PreventivoVarianti.query.filter_by(tipologia='varianti', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def get_counter_preventivi_per_numero(numero_preventivo):
        q = PreventivoVarianti.query.filter_by(tipologia='varianti', numero_preventivo=numero_preventivo)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def chiudiPreventivo(numero_preventivo):

        preventivi = PreventivoVarianti.query.filter_by(numero_preventivo=numero_preventivo, tipologia='varianti').order_by(
            desc(PreventivoVarianti.data)).all()

        primo_giro = True

        for prev in preventivi:
            if primo_giro:
                primo_giro = False
                prev.stato = False
                PreventivoVarianti.commit()

            else:
                PreventivoVarianti.delRow(prev)

    def stampaPreventivo(numero_preventivo, data, iva, tipoSconto, sconto, chiudiPreventivo, acorpo):

        if chiudiPreventivo:
            PreventivoVarianti.chiudiPreventivo(numero_preventivo)

        scontoDaApplicare = sconto

        preventivo = PreventivoVarianti.query.filter_by(tipologia='varianti', numero_preventivo=numero_preventivo,
                                                     data=data).first()

        dipendente = Dipendente.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        infoPreventivo = PreventivoVarianti.returnSinglePreventivo(numero_preventivo=numero_preventivo, data=data)

        codicePrev = PreventivoVarianti.calcolaCodicePreventivoNoObj(numero_preventivo, data)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=preventivo.intervento_commessa).first()

        contaLavorazioni = 0

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        latexScript = '''
                        \\documentclass[a4paper]{article}
                        \\usepackage{graphicx}
                        \\graphicspath{ {./Immagini/} }
                        \\usepackage{setspace}
                        \\usepackage{eurosym}
                        \\usepackage{xcolor}
                        \\usepackage{tabularx}
                        \\usepackage[top=1.7cm, bottom=1.7cm, left=2.6cm, right=2.6cm]{geometry}

                        \\usepackage{fancyhdr}
                        \\pagestyle{fancy}
                        \\lhead{}
                        \\chead{} 
                      '''

        latexScript += '\\rhead{US' + codicePrev + 'V}'

        latexScript += '''
                        \\lfoot{\\thepage}
                        \\cfoot{
                            \\begin{spacing}{0.5}
                            {\\scriptsize
                              \\textbf{UnionService Srl.} Via Roma n. 84 - 37060 Castel d'Azzano (VR) - Tel. +39 045 8521697 - Fax +39 045 8545123 \\\\
                              Cell. +39 342 7663538 - C.F./P.iva 04240420234 - REA: VR-404097
                            }
                            \\end{spacing}
                        }
                        \\rfoot{}
                        \\renewcommand{\\headrulewidth}{0pt}
                        \\renewcommand{\\footrulewidth}{0.4pt}

                        \\usepackage{array}
                        \\usepackage{ragged2e}
                        \\newcolumntype{R}[1]{>{\\RaggedLeft\\hspace{0pt}}p{#1}}
                        \\newcolumntype{L}[1]{>{\\RaggedRight\\hspace{0pt}}p{#1}}

                        \\renewcommand{\\arraystretch}{0}

                        \\begin{document}

                        \\begin{figure}[!t]
                        \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                        \\end{figure}

                        \\noindent\\begin{tabular}{| L{72.2mm} |}
                            \\hline
                            \\vspace{2.5mm}
                            \\begin{spacing}{0}
                            \\textbf{COMMESSA}
                            \\end{spacing}\\\\
                            \\hline
                            \\vspace{4mm}
                            \\begin{spacing}{1.2}

                        '''
        latexScript += commessa.intervento.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                                  "\\'u").replace(
            "ì", "\\'i") + ' \\newline '
        latexScript += commessa.indirizzo.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                                 "\\'u").replace(
            "ì", "\\'i") + ' \\newline ' + commessa.comune.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                             "\\'o").replace(
            "ù", "\\'u").replace("ì", "\\'i")
        latexScript += '''
                          \\end{spacing}\\\\
                            \\hline
                          \\end{tabular}
                          \\quad
                          \\begin{tabular}{ | R{72.2mm} | }
                            \\hline
                            \\vspace{2.5mm}
                            \\begin{spacing}{0}
                            \\textbf{CLIENTE}
                            \\end{spacing}\\\\
                            \\hline
                            \\vspace{4mm}
                            \\begin{spacing}{1.2}

                       '''
        latexScript += cliente.nome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                           "\\'u").replace(
            "ì", "\\'i") + ' ' + cliente.cognome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace(
            "ù", "\\'u").replace("ì", "\\'i") + ' \\newline '
        latexScript += 'tel. ' + str(cliente.telefono) + ' \\newline '
        latexScript += cliente.indirizzo.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                                "\\'u").replace(
            "ì", "\\'i")

        latexScript += '''
                          \\end{spacing}\\\\
                            \\hline
                          \\end{tabular}

                          \\begin{center}
                          \\begin{tabular}{|L{89mm} R{60mm}| }
                          \\hline
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Preventivo Varianti}
                          \\end{spacing}&
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}

                     '''

        latexScript += oggi

        latexScript += '''

                          \\end{spacing}\\\\
                          \\hline
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Validit\\'a:}
                       '''
        validita= datetime.timedelta(days=30) + datetime.datetime.now()

        validita = "{}/{}/{}".format(validita.day, validita.month, validita.year)

        latexScript += validita
        latexScript += '''
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Operatore:}

                       '''

        latexScript += dipendente.nome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                              "\\'u").replace(
            "ì", "\\'i") + ' ' + dipendente.cognome.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                      "\\'o").replace(
            "ù", "\\'u").replace("ì", "\\'i")

        latexScript += '''
                          \\end{spacing} \\\\
                          \\hline
                          \\end{tabular}
                          \\end{center}

                          \\noindent\\begin{tabular}{ | L{10mm} |  L{86mm} | L{12mm} | L{12mm} | L{16mm} | }
                          \\hline
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Pos.}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Descrizione}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Qnt.}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{U.M.}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Importo}
                          \\end{spacing} \\\\
                          \\hline
                          %FINE HEADER
                       '''

        totalePreventivo = 0

        for lav in infoPreventivo[1]:
            contaLavorazioni += 1
            latexScript += '''
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''
            latexScript += '{}'.format(contaLavorazioni)

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            latexScript += lav[0].tipologia_lavorazione.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                          "\\'o").replace(
                "ù", "\\'u").replace("ì", "\\'i")

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if acorpo:
                latexScript += '-'
            else:
                latexScript += '{}'.format(lav[1])

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if acorpo:
                latexScript += 'a corpo'
            else:
                latexScript += lav[0].unitaMisura

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                                \\euro\\hfill 
                            '''
            latexScript += '{}'.format(lav[2])
            totalePreventivo += lav[2]

            latexScript += '''
                              \\end{spacing} \\\\
                              \\hline
                              %FINE RIGA

                            '''

        latexScript += '''
                          \\end{tabular}

                          \\noindent\\begin{tabular}{|L{108.5mm} | L{8mm} | L{8mm} |  L{16mm}| }
                          \\hline
                          \\multicolumn{3}{ | L{124.5mm} | }{
                            \\vspace{2.5mm}
                            \\begin{spacing}{0}
                              \\textbf{Totale imponibile}
                            \\end{spacing}
                          } &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\euro\\hfill
                       '''
        latexScript += '{}'.format(totalePreventivo)

        totaleScontato = totalePreventivo
        laberForSconto = ""

        if tipoSconto == 2:
            totaleScontato -= sconto;
            laberForSconto = "Sconto netto"
        elif tipoSconto == 3:
            totaleScontato += totalePreventivo * sconto / 100
            laberForSconto = "\%"
        elif tipoSconto == 4:
            totaleScontato = sconto
            laberForSconto = "Sconto"

        totaleConIva = totaleScontato + (totaleScontato * iva / 100)

        totaleScontato = math.floor(totaleScontato * 100) / 100
        totaleConIva = math.floor(totaleConIva * 100) / 100

        latexScript += '''
                          \\end{spacing}\\\\
                          \\hline
                          \\multicolumn{1}{  L{108.5mm} | }{} &
                          \\multicolumn{2}{  L{16mm} | }{
                            \\vspace{2.5mm}
                            \\begin{spacing}{0}
                        '''

        latexScript += '\\textbf{' + laberForSconto + '}'

        latexScript += '''
                            \\end{spacing}
                          } &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                          \\euro\\hfill 
                       '''

        latexScript += '{}'.format(totaleScontato)

        latexScript += '''
                          \\end{spacing}\\\\
                          \\cline{2-4}
                          \\multicolumn{1}{  L{108.5mm} | }{} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{IVA}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                        '''
        latexScript += '\\textbf{' + str(iva) + '\%}'

        latexScript += '''
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                          \\euro\\hfill
                        '''

        latexScript += '{}'.format(totaleConIva)

        latexScript += '''
                          \\end{spacing}\\\\
                          \\cline{2-4}
                          \\end{tabular}

                       '''

        latexScript += '''
                      \\vspace{19mm}


                      \\begin{center}
                      \\begin{tabular}{|L{105mm} | L{44mm}| }
                      \\hline
                      \\begin{spacing}{0.3}
                        \\textbf{NOTE} \\newline
                        \\hfill
                        Bho ricordati di fare qualcosa del tipo dell'esempio sai

                      \\end{spacing}&
                      \\begin{spacing}{0.3}
                      \\textbf{Firma per accettazione}
                      \\end{spacing}\\\\
                      \\hline
                      \\end{tabular}
                      \\end{center}

                      \\newpage

                      \\begin{figure}[!t]
                      \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                      \\end{figure}

                      \\begin{itemize}
                          \\item \\textbf{Ipotizzati \\euro 2.500,00 per smaltimenti materiali}
                      \\end{itemize}

                      \\noindent\\textbf{Dalla seguente offera sono escluse:}
                      \\begin{itemize}
                          \\item IVA e qualsiasi altro onere fiscale;
                          \\item Ore in economia per opere extra-capitolato (\\euro/h 23,00);
                          \\item Costi di energia elettrica e acqua ad uso cantiere;
                          \\item Qualsiasi altra voce non citata;
                          \\item Sul totale preventivato ci si riserva di un errore del 5\\% come imprevisti cantiere;
                          \\item Pratica per detrazioni fiscali da quantificare;
                      \\end{itemize}

                      \\noindent\\textbf{Pagamenti}
                      \\begin{itemize}
                          \\item Da concordare in fase di accetazione.
                      \\end{itemize}

                      \\textcolor{red}{La presente offerta ha validit\'a 30 giorni dalla data odierna.}\\\\

                      Castel d'Azzano, il 11 - 7 - 2018
                      \\vspace{1cm}\\\\
                      Per accettazione ..............................................................

                    \\end{document}

                       '''

        with open('app/preventiviLatexDir/preventivoVarianti.tex', mode='w') as prova:
            prova.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex preventivoVarianti.tex")