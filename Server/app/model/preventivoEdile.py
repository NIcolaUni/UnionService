from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.dipendenteDBmodel import DipendenteDBmodel
from .db.lavorazioniPreventivoEdile.lavorazionePreventivoDBmodel import LavorazionePreventivoDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneCorpoDBmodel import SottolavorazioneCorpoDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneCadDBmodel import SottolavorazioneCadDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMlDBmodel import SottolavorazioneMlDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMqDBmodel import SottolavorazioneMqDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMcDBmodel import SottolavorazioneMcDBmodel
from .clienteAccolto import  ClienteAccolto
from sqlalchemy import desc, func
import datetime
import app
import os
import math

class __SottolavorazioneCorpoPreventivo__(SottolavorazioneCorpoDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

class __SottolavorazioneCadPreventivo__(SottolavorazioneCadDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, prezzoBase):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero


class __SottolavorazioneMlPreventivo__(SottolavorazioneMlDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, prezzoBase ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza



class __SottolavorazioneMqPreventivo__(SottolavorazioneMqDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza, prezzoBase ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza



class __SottolavorazioneMcPreventivo__(SottolavorazioneMcDBmodel):
    def __init__(self, numero_preventivo, data, ordine, ordine_sottolavorazione, numero, larghezza, altezza, profondita, prezzoBase ):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita


class __LavorazionePreventivo__(LavorazionePreventivoDBmodel):
    def __init__(self,  numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario):
        self.numero_preventivo=numero_preventivo
        self.data = data
        self.ordine = ordine
        self.tipologia = 'edile'

        self.settore = settore
        self.tipologia_lavorazione = tipologia_lavorazione
        self.nome_modificato = tipologia_lavorazione
        self.unitaMisura=unitaMisura
        self.prezzoUnitario=prezzoUnitario

class __Commessa__(CommessaDBmodel):
    def __init__(self, numero_preventivo, intervento, indirizzo, comune):
        self.numero_preventivo = numero_preventivo
        self.intervento = intervento
        self.indirizzo = indirizzo
        self.comune = comune

class PreventivoEdile(PreventivoDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, intervento_commessa, indirizzo_commessa,  comune_commessa,
                 stato=True, note=None):

        oldCommessa = __Commessa__.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=intervento_commessa).first()

        if oldCommessa is None:
            commessa = __Commessa__(numero_preventivo=numero_preventivo, intervento=intervento_commessa,
                                    indirizzo=indirizzo_commessa, comune=comune_commessa)
            __Commessa__.addRow(commessa)

        self.numero_preventivo=numero_preventivo
        self.data = data
        self.tipologia='edile'
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.intervento_commessa=intervento_commessa
        self.stato = stato
        self.note = note



    def calcolaCodicePreventivo(self):
        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo)+dipendente+str(annoPreventivo)

    def calcolaCodicePreventivoNoObj(numero_preventivo, data):

        prev = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='edile').first()

        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = prev.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = prev.dipendente_generatore.split('_')[1][0:3].upper()

        return str(prev.numero_preventivo)+dipendente+str(annoPreventivo)

    def registraPreventivo( nome_cliente, cognome_cliente, indirizzo_cliente ,
                            dipendente_generatore, intervento_commessa,
                            indirizzo_commessa, comune_commessa):

        youngerPrev = PreventivoDBmodel.query.order_by(desc(PreventivoDBmodel.numero_preventivo)).first()
        lastNumPrev=99

        #se ci sono gia' preventivi registrati prende il numero_preventivo del piu' recente
        if youngerPrev is not None:
            lastNumPrev=youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoEdile(numero_preventivo=lastNumPrev+1, data=oggi, nome_cliente=nome_cliente,
                                     cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=intervento_commessa, indirizzo_commessa=indirizzo_commessa,
                                     comune_commessa=comune_commessa)

        PreventivoDBmodel.addRow(preventivo)

        return ( lastNumPrev+1, oggi )

    def eliminaPreventivo(numero_preventivo, data):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='edile').first()

        PreventivoDBmodel.delRow(toDel)

    def __duplicaSottolavorazioni__(sottolavorazioni, unitaMisura):

        returnList = []

        if unitaMisura == 'cad':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneCadPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                                data=sottolav.data, ordine=sottolav.ordine,
                                                                ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                                numero=sottolav.numero)
                returnList.append(newSottolav)

        elif unitaMisura == 'ml':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMlPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza)
                returnList.append(newSottolav)

        elif unitaMisura == 'mq':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMqPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza)
                returnList.append(newSottolav)

        elif unitaMisura == 'mc':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMcPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               data=sottolav.data, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, profondita=sottolav.profondita)
                returnList.append(newSottolav)

        elif unitaMisura == 'corpo':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneCorpoPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                                data=sottolav.data, ordine=sottolav.ordine,
                                                                ordine_sottolavorazione=sottolav.ordine_sottolavorazione)
                returnList.append(newSottolav)

        return returnList

    def __duplicaLavorazioni__(lavorazioni):

        returnList = []
        for lav in lavorazioni:
            newLav = __LavorazionePreventivo__(numero_preventivo=lav.numero_preventivo, data=lav.data,
                                               ordine=lav.ordine,
                                               settore=lav.settore, tipologia_lavorazione=lav.tipologia_lavorazione,
                                               unitaMisura=lav.unitaMisura, prezzoUnitario=lav.prezzoUnitario)
            returnList.append(newLav)

        return returnList

    def inserisciNote(numero_preventivo, data, nota):
        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                  tipologia='edile').update({'note': nota})

        PreventivoDBmodel.commit()

    def modificaPreventivo(numero_preventivo, data, dipendente_generatore):
        '''
         Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento,
         ne fa una copia ( compresa di lavorazioni e sottolavorazioni ) cambiando unicamente
         gli attributi "data", settata alla data odierna, e "dipendente_ultimaModifica", settato con lo username
         del dipendente che sta facendo la modifica.

        :param numero_preventivo, dipendente_ultimaModifica:
        :return:
        '''



        lastPrev = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='edile').first()
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        #se il preventivo viene modificato piu' volte lo stesso giorno non viene fatta alcuna copia "

        if str(now).split(' ')[0] == str(lastPrev.data):

            return (numero_preventivo, oggi)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=lastPrev.intervento_commessa).first()

        preventivo = PreventivoEdile(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=commessa.intervento,
                                     indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune )


        PreventivoDBmodel.addRowNoCommit(preventivo)
        PreventivoDBmodel.commit()

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()


        lavorazioni = PreventivoEdile.__duplicaLavorazioni__(lavorazioni)

        for lav in lavorazioni:
            lav.data = oggi
            PreventivoDBmodel.addRowNoCommit(lav)

        PreventivoEdile.commit()

        sottolavorazioniCad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniCad = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniCad, 'cad')

        sottolavorazioniMl = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMl = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMl, 'ml')

        sottolavorazioniMq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMq = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMq, 'mq')

        sottolavorazioniMc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniMc = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMc, 'mc')

        sottolavorazioniCorpo = __SottolavorazioneCorpoPreventivo__.query.filter_by(
            numero_preventivo=lastPrev.numero_preventivo, data=lastPrev.data).all()

        sottolavorazioniCorpo = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniCorpo, 'a corpo')

        sottolavorazioni = sottolavorazioniCad + sottolavorazioniMl + sottolavorazioniMc + sottolavorazioniMq + sottolavorazioniCorpo

        for sottoLav in sottolavorazioni:
            sottoLav.data= oggi
            PreventivoDBmodel.addRowNoCommit(sottoLav)

        PreventivoEdile.commit()

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
                                        numero, prezzoBase, larghezza=None, altezza=None, profondita=None):

        lavorazione = None
        if unitaMisura == 'cad':
            lavorazione = __SottolavorazioneCadPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione, numero=numero,
                                                             prezzoBase=prezzoBase)
        elif unitaMisura == 'ml':
            lavorazione = __SottolavorazioneMlPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, prezzoBase=prezzoBase )

        elif unitaMisura == 'mq':
            lavorazione = __SottolavorazioneMqPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, prezzoBase=prezzoBase )

        elif unitaMisura == 'mc':
            lavorazione = __SottolavorazioneMcPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita,
                                                           prezzoBase=prezzoBase)
        elif unitaMisura == 'a corpo':
            lavorazione = __SottolavorazioneCorpoPreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                            ordine=ordine,
                                                            ordine_sottolavorazione=ordine_sottolavorazione)

        PreventivoDBmodel.addRow(lavorazione)


    def nuovaSottolavorazione(numero_preventivo, data, ordine):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first().unitaMisura
        prezzoBase = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first().prezzoUnitario

        if unitaMisura == 'cad':
            last_sottolav_cad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                  data=data, ordine=ordine).order_by( desc(__SottolavorazioneCadPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                             ordine=ordine, ordine_sottolavorazione=last_sottolav_cad+1, numero=1, prezzoBase=prezzoBase )
        elif unitaMisura == 'ml':
            last_sottolav_ml = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMlPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_ml+1,
                                                         numero=1, larghezza=1, prezzoBase=prezzoBase)

        elif unitaMisura == 'mq':
            last_sottolav_mq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMqPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mq+1,
                                                         numero=1, larghezza=1, altezza=1, prezzoBase=prezzoBase)


        elif unitaMisura == 'mc':
            last_sottolav_mc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by( desc(__SottolavorazioneMcPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mc+1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1, prezzoBase=prezzoBase)

        elif unitaMisura == 'a corpo':
            last_sottolav_corpo = __SottolavorazioneCorpoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                data=data, ordine=ordine).order_by(
                desc(__SottolavorazioneCorpoPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data,
                                                         unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_corpo + 1)


    def registraLavorazione( numero_preventivo, data, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario,
                             numero, larghezza=None, altezza=None, profondita=None ):

        controlVar = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:
            lavorazione = __LavorazionePreventivo__(numero_preventivo=numero_preventivo, data=data,
                                                    ordine=ordine, settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                                    unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario)
            PreventivoDBmodel.addRow(lavorazione)
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
            elif unitaMisura == 'a corpo':
                ordineSottolavorazione = PreventivoEdile.__calcolcaOrdineSottolavorazione__(
                    queryClass=__SottolavorazioneCorpoPreventivo__.query,
                    numero_preventivo=numero_preventivo, data=data,
                    ordine=ordine)

        PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, data=data, unitaMisura=unitaMisura,
                                                     ordine=ordine, ordine_sottolavorazione=ordineSottolavorazione,
                                                     numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita,
                                                     prezzoBase=prezzoUnitario)


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
        elif unitaMisura == 'a corpo':
            toDel = __SottolavorazioneCorpoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                                     ordine=ordine,
                                                                     ordine_sottolavorazione=ordine_sottolavorazione).first()

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

            PreventivoDBmodel.commit()


    def modificaOrdineLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, data, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()

    def __settaOrdineSottolavorazioneNegativo__(sottolavorazione, queryClass):

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

        elif unitaMisura == 'a corpo':
            queryClassSottolavorazione = __SottolavorazioneCorpoPreventivo__.query

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
            for lav in sottolavPrev:
                PreventivoEdile.__settaOrdineSottolavorazioneNegativo__(lav, queryClassSottolavorazione)

            PreventivoDBmodel.commit()



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

        elif unitaMisura == 'a corpo':
            __SottolavorazioneCorpoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        PreventivoDBmodel.commit()
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

        elif unitaMisura == 'a corpo':
            __SottolavorazioneCorpoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=ordine_sottolavorazione).update(
                modifica)

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

                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += sottolav.numero
                    sommaPrezziSottolav += sottolav.numero * sottolav.prezzoBase

                #prezzoTotale = quantitaTotale * lav.prezzoUnitario
                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'ml':
                sottolavorazioni = __SottolavorazioneMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMlPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza) * sottolav.prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


            elif lav.unitaMisura == 'mq':
                sottolavorazioni = __SottolavorazioneMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMqPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza)*sottolav.prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))



            elif lav.unitaMisura == 'mc':
                sottolavorazioni = __SottolavorazioneMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)*sottolav.prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'a corpo':
                sottolavorazioni = __SottolavorazioneCorpoPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        data=data, ordine=lav.ordine).order_by(
                                        __SottolavorazioneCorpoPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += 1

                prezzoTotale = quantitaTotale * lav.prezzoUnitario

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

        return ( ordineSettori, resultLav)

    def returnLastPreventivoCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        last_prev = PreventivoEdile.query.filter_by(tipologia='edile', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(desc(PreventivoEdile.data), desc(PreventivoEdile.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=last_prev.numero_preventivo, data=last_prev.data)


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
                 chiamata a PreventivoEdile.returnSinglePreventivo()
        '''

        preventivi = PreventivoEdile.query.filter_by(tipologia='edile', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(
                                                        PreventivoEdile.numero_preventivo, desc(PreventivoEdile.data)).all()

        returnList = []

        for prev in preventivi:
            returnList.append( ( prev, PreventivoEdile.returnSinglePreventivo(numero_preventivo=prev.numero_preventivo, data=prev.data)) )

        return returnList

    def get_counter_preventivi_per_cliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        q = PreventivoEdile.query.filter_by(tipologia='edile', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def get_counter_preventivi_per_numero(numero_preventivo):
        q = PreventivoEdile.query.filter_by(tipologia='edile', numero_preventivo=numero_preventivo)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def chiudiPreventivo(numero_preventivo):

        preventivi= PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, tipologia='edile').order_by(desc(PreventivoEdile.data)).all()

        primo_giro = True

        for prev in preventivi:
            if primo_giro:
                primo_giro=False
                prev.stato=False
                PreventivoEdile.commit()

            else:
                PreventivoEdile.delRow(prev)

    def __calcolaIndiceLastLavorazionePagineIntermedie__(startingIndex, grandezzaRighe):

        index = startingIndex
        tmpGrandezzaRighe = 0

        for lunghezza in grandezzaRighe:

            tmpGrandezzaRighe += lunghezza

            if tmpGrandezzaRighe <= 21.6:
                index += 1

            else:
                break

        if tmpGrandezzaRighe <= 18:
            return [index, False]
        else:
            return [index, True]

    def __calcoraIndiceLastLavorazionePrimaPagina__(grandezzaRighe):
        index = -1
        tmpGrandezzaRighe = 0

        for lunghezza in grandezzaRighe:

            tmpGrandezzaRighe += lunghezza

            if tmpGrandezzaRighe <= 11.7:
                index += 1

            else:
                break

        if tmpGrandezzaRighe <= 9:
            return [index, False]
        else:
            return [index, True]


    def __calcolaLavorazioniPerPaginaPreventivo__(lavorazioni):
        '''

        Una lavorazione il cui nome occupa una sola riga è altra 0.9 cm ed ogni riga extra aggiunge un 0.4cm;
        Una lavorazione occupa una sola riga se il suo numero di caratteri <= 50.
        Per quanto riguarda la prima facciata, un insieme di lavorazioni sta tutto
        in una pagina ( compreso del totale ) se l'altezza dell'insieme di
        righe delle lavorazioni ( escluso il totale ) è <= 9cm; se la riga dello sconto non compare il limite di
        9cm si trasforma in 9.9cm. Se l'insieme di lavorazioni supera questo limite allora nella prima facciata
        l'insieme delle lavorazioni non potrà superare gli 11.7 cm.
        Nelle pagine successive alla prima, se il totale è presente, il numero di righe avrà come limite i 18cm
        mentre, se il totale va su un'altra pagina ancora, sarà di 21.6cm.
        Se il totale finisce sull'ultima pagina assieme ad esso potremmo avere al massimo un numero di lavorazioni
        che non superi i 4.5cm;


        :return: ritorna una tupla di due elementi dove_
                -prima pos: una lista dove il numero di elementi indica il numero di pagine necessarie per
                            stampare il preventivo e ogni elemento indica il numero dell'ultima lavorazione
                            nella pagina;
                -seconda pos: un booleano indicante se nell'ultima pagina il numero di lavorazioni supera i 4.5cm

        '''

        grandezzaRighe = []

        #Per ogni lavorazione calcolo l'altezza della corrispondente riga nel preventivo
        for lav in lavorazioni:
            numeroRighe = int(len( lav[0].nome_modificato )/50)
            resto = len( lav[0].nome_modificato )%50

            lunghezzaRigaCm = 0

            if numeroRighe <= 1:
                lunghezzaRigaCm = 0.9

            else:
                addedCm = 0
                for i in range( 1, numeroRighe):
                    addedCm += 0.4

                lunghezzaRigaCm = 0.9+addedCm

            if numeroRighe >= 1 and resto > 0:
                lunghezzaRigaCm += 0.4

            grandezzaRighe.append(round(lunghezzaRigaCm*100)/100)

        if len(grandezzaRighe) > 0:
            indexesToRet = []
            numPag = 1

            index, continua = PreventivoEdile.__calcoraIndiceLastLavorazionePrimaPagina__(grandezzaRighe)


            indexesToRet.append(index)

            while continua and index+1 < len(grandezzaRighe):

                index, continua = PreventivoEdile.__calcolaIndiceLastLavorazionePagineIntermedie__(index, grandezzaRighe[index+1:len(grandezzaRighe)])
                indexesToRet.append(index)
                numPag += 1

            if continua:
                numPag += 1


            if len(indexesToRet) < numPag:
                indexesToRet.append(len(grandezzaRighe)-1)

            totLunghezzaUltimaPag = 0

            for lunghezza in grandezzaRighe[indexesToRet[-2]:indexesToRet[-1]]:
                totLunghezzaUltimaPag+=lunghezza

            if totLunghezzaUltimaPag <= 4.5:
                return ( indexesToRet, False )
            else:
                return ( indexesToRet, True )

        else:
            return ([], False)



    def stampaPreventivo(numero_preventivo, data, iva, tipoSconto, sconto, chiudiPreventivo, sumisura ):

        preventivo = PreventivoEdile.query.filter_by(tipologia='edile', numero_preventivo=numero_preventivo,
                                                     data=data).first()

        dipendente = DipendenteDBmodel.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        infoPreventivo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=numero_preventivo, data=data)

        codicePrev = PreventivoEdile.calcolaCodicePreventivoNoObj(numero_preventivo, data)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo, intervento=preventivo.intervento_commessa).first()

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
                        \\usepackage[top=1.7cm, bottom=4.5cm, left=2.6cm, right=2.6cm]{geometry}

                        \\usepackage{fancyhdr}
                        \\pagestyle{fancy}
                        \\lhead{}
                        \\chead{} 
                      '''

        latexScript += '\\rhead{US' + codicePrev + 'E}'

        latexScript += '''
                        \\cfoot{
                                {\\normalsize
                                  \\begin{center}
                                  \\begin{tabular}{|L{105mm} | L{44mm}| }
                                  \\hline
                                  \\begin{spacing}{0.3}
                                    \\textbf{NOTE} \\newline
                                    \\hfill
                                    {\\centering
                        '''
        if preventivo.note is not None:
            latexScript += preventivo.note

        latexScript +=  '''
                                    }
                                  \\end{spacing}&
                                  \\begin{spacing}{0.3}
                                  \\textbf{Firma per accettazione}
                                  \\end{spacing}\\\\
                                  \\hline
                                  \\end{tabular}
                                  \\end{center}
                                  \\noindent\\rule{\\textwidth}{0.4pt}
                                }
                                {\\footnotesize
                                  \\raggedright\\thepage \\\\ \\centering\\textbf{UnionService Srl.} Via Roma n. 84 - 37060 Castel d'Azzano (VR) - Tel. +39 045 8521697 - Fax +39 045 8545123 \\\\
                                  Cell. +39 342 7663538 - C.F./P.iva 04240420234 - REA: VR-404097
                                }
                        }
                        \\rfoot{}
                        \\renewcommand{\\headrulewidth}{0pt}

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
                            \\textbf{Preventivo Edile}
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
        validita = datetime.timedelta(days=30) + datetime.datetime.now()

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

        numPagine = PreventivoEdile.calcolaLunghezzaPreventivo(infoPreventivo[1])

        #############################################################

        totalePreventivo = 0

        for lav in infoPreventivo[1]:
            contaLavorazioni += 1
            latexScript += '''
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''
            latexScript += '{} - {}'.format(contaLavorazioni, numPagine[contaLavorazioni-1])

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            latexScript += lav[0].nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                    "\\'o").replace("ù",
                                                                                                                    "\\'u").replace(
                "ì", "\\'i")

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += '{}'.format(lav[1])
            else:
                latexScript += '-'

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += lav[0].unitaMisura

            else:
                latexScript += 'a corpo'

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

        latexScript += '''
                          \\end{spacing}\\\\
                          \\hline
                       '''

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
            laberForSconto = "Totale con sconto"

        totaleConIva = totaleScontato + (totaleScontato * iva / 100)

        totaleScontato = math.floor(totaleScontato * 100) / 100
        totaleConIva = math.floor(totaleConIva * 100) / 100

        if tipoSconto != 1:
            latexScript += '''
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

            latexScript += '{}'.format(totaleScontato) + '\\end{spacing}\\\\ \\cline{2-4}'

        latexScript += '''
                          \\multicolumn{1}{  L{108.5mm} | }{} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{IVA}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                        '''

        if iva == 0:
            latexScript += '\\textbf{\%}'
        else:
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
                      \\begin{figure}[!t]
                      \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                      \\end{figure}

                      \\newpage
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
                          \\item Da concordare in fase di accettazione.
                      \\end{itemize}

                      \\textcolor{red}{La presente offerta ha validit\'a 30 giorni dalla data odierna.}\\\\

                      Castel d'Azzano, il 11 - 7 - 2018
                      \\vspace{1cm}\\\\
                      Per accettazione ..............................................................

                    \\end{document}

                       '''

        with open('app/preventiviLatexDir/preventivoEdile.tex', mode='w') as prova:
            prova.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex preventivoEdile.tex")

    #############################################################################

    def OldstampaPreventivo(numero_preventivo, data, iva, tipoSconto, sconto, chiudiPreventivo, sumisura ):


        if chiudiPreventivo :
            PreventivoEdile.chiudiPreventivo(numero_preventivo)


        preventivo = PreventivoEdile.query.filter_by(tipologia='edile', numero_preventivo=numero_preventivo,
                                                     data=data).first()

        dipendente = DipendenteDBmodel.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        infoPreventivo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=numero_preventivo, data=data)

        codicePrev = PreventivoEdile.calcolaCodicePreventivoNoObj(numero_preventivo, data)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo, intervento=preventivo.intervento_commessa).first()

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

        latexScript += '\\rhead{US'+codicePrev+'E}'



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
        latexScript += commessa.intervento.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i") +' \\newline '
        latexScript += commessa.indirizzo.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i") + ' \\newline ' +  commessa.comune.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i")
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
        latexScript += cliente.nome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i") + ' '+ cliente.cognome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i") + ' \\newline '
        latexScript += 'tel. '+ str(cliente.telefono) + ' \\newline '
        latexScript += cliente.indirizzo.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i")

        latexScript+= '''
                          \\end{spacing}\\\\
                            \\hline
                          \\end{tabular}
                        
                          \\begin{center}
                          \\begin{tabular}{|L{89mm} R{60mm}| }
                          \\hline
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Preventivo Edile}
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
        validita = datetime.timedelta(days=30) + datetime.datetime.now()

        validita = "{}/{}/{}".format(validita.day, validita.month, validita.year)

        latexScript += validita
        latexScript += '''
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{Operatore:}

                       '''

        latexScript += dipendente.nome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i") + ' ' + dipendente.cognome.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i")

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
            contaLavorazioni+=1
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

            latexScript += lav[0].nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù", "\\'u").replace("ì", "\\'i")

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += '{}'.format(lav[1])
            else:
                latexScript += '-'


            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += lav[0].unitaMisura

            else:
                latexScript += 'a corpo'


            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                                \\euro\\hfill 
                            '''
            latexScript += '{}'.format(lav[2])
            totalePreventivo += lav[2]

            latexScript +=  '''
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

        latexScript += '''
                          \\end{spacing}\\\\
                          \\hline
                       '''

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
            laberForSconto = "Totale con sconto"

        totaleConIva = totaleScontato + (totaleScontato * iva / 100)

        totaleScontato = math.floor(totaleScontato * 100) / 100
        totaleConIva = math.floor(totaleConIva * 100) / 100


        if tipoSconto != 1:
            latexScript += '''
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

            latexScript += '{}'.format(totaleScontato)+'\\end{spacing}\\\\ \\cline{2-4}'


        latexScript += '''
                          \\multicolumn{1}{  L{108.5mm} | }{} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                            \\textbf{IVA}
                          \\end{spacing} &
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                        '''

        if iva == 0:
            latexScript += '\\textbf{\%}'
        else:
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
                      '''

        if preventivo.note is not None:
            latexScript += preventivo.note

        latexScript += '''
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


        with open('app/preventiviLatexDir/preventivoEdile.tex', mode='w') as prova:
            prova.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex preventivoEdile.tex")