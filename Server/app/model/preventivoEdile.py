from .db.lavorazioneEdileDBmodel import LavorazioneEdileDBmodel
from .db.prezzarioEdileDBmodel import PrezzarioEdileDBmodel
from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.dipendenteDBmodel import DipendenteDBmodel
from .db.lavorazioniPreventivoEdile.lavorazionePreventivoDBmodel import LavorazionePreventivoDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneCadDBmodel import SottolavorazioneCadDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMlDBmodel import SottolavorazioneMlDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMqDBmodel import SottolavorazioneMqDBmodel
from .db.lavorazioniPreventivoEdile.sottolavorazioni.sottolavorazioneMcDBmodel import SottolavorazioneMcDBmodel
from .pagamentiCliente import PagamentiCliente
from .clienteAccolto import  ClienteAccolto
from sqlalchemy import desc, func
import datetime
import app
import os
import math


class __SottolavorazioneCadPreventivo__(SottolavorazioneCadDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione, numero, prezzoBase, ricarico):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico


class __SottolavorazioneMlPreventivo__(SottolavorazioneMlDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione, numero, larghezza, prezzoBase, ricarico ):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico



class __SottolavorazioneMqPreventivo__(SottolavorazioneMqDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione, numero, larghezza, altezza, prezzoBase, ricarico ):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico



class __SottolavorazioneMcPreventivo__(SottolavorazioneMcDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione, numero, larghezza, altezza, profondita, prezzoBase, ricarico ):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico


class __LavorazionePreventivo__(LavorazionePreventivoDBmodel):
    def __init__(self,  numero_preventivo, revisione, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
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
                 ricarico_generale,
                 stato=True, note=None, revisione=1):

        oldCommessa = __Commessa__.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=intervento_commessa).first()

        if oldCommessa is None:
            commessa = __Commessa__(numero_preventivo=numero_preventivo, intervento=intervento_commessa,
                                    indirizzo=indirizzo_commessa, comune=comune_commessa)
            __Commessa__.addRow(commessa)

        self.numero_preventivo=numero_preventivo
        self.data = data
        self.data_ultima_modifica = data
        self.tipologia='edile'
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.intervento_commessa=intervento_commessa
        self.stato = stato
        self.note = note
        self.revisione = revisione
        self.ricarico_generale = ricarico_generale



    def calcolaCodicePreventivo(self):
        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo)+dipendente+str(annoPreventivo)

    def calcolaCodicePreventivoNoObj(numero_preventivo, revisione):

        prev = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='edile').first()


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
        ricaricoFromPrezzario = PrezzarioEdileDBmodel.query.first().ricaricoAzienda

        #se ci sono gia' preventivi registrati prende il numero_preventivo del piu' recente
        if youngerPrev is not None:
            lastNumPrev=youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoEdile(numero_preventivo=lastNumPrev+1, data=oggi, nome_cliente=nome_cliente,
                                     cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=intervento_commessa, indirizzo_commessa=indirizzo_commessa,
                                     comune_commessa=comune_commessa, revisione=1, ricarico_generale=ricaricoFromPrezzario)

        PreventivoDBmodel.addRow(preventivo)

        return ( lastNumPrev+1, 1 )

    def modificaRicaricoGenerale(numero_preventivo, revisione, ricarico):

        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).update({'ricarico_generale':ricarico})

        PreventivoEdile.commit()

    def eliminaPreventivo(numero_preventivo, revisione):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='edile').first()

        PreventivoDBmodel.delRow(toDel)

    def __duplicaSottolavorazioni__(sottolavorazioni, unitaMisura ):

        returnList = []

        if unitaMisura == 'cad':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneCadPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                                revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                                ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                                numero=sottolav.numero, prezzoBase=sottolav.prezzoBase,
                                                                ricarico=sottolav.ricarico)
                returnList.append(newSottolav)

        elif unitaMisura == 'ml':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMlPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               prezzoBase=sottolav.prezzoBase, ricarico=sottolav.ricarico)
                returnList.append(newSottolav)

        elif unitaMisura == 'mq':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMqPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, prezzoBase=sottolav.prezzoBase,
                                                               ricarico=sottolav.ricarico)
                returnList.append(newSottolav)

        elif unitaMisura == 'mc':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMcPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, profondita=sottolav.profondita,
                                                               prezzoBase=sottolav.prezzoBase, ricarico=sottolav.ricarico)
                returnList.append(newSottolav)


        return returnList

    def __duplicaLavorazioni__(lavorazioni):

        returnList = []
        for lav in lavorazioni:
            newLav = __LavorazionePreventivo__(numero_preventivo=lav.numero_preventivo, revisione=lav.revisione,
                                               ordine=lav.ordine,
                                               settore=lav.settore, tipologia_lavorazione=lav.tipologia_lavorazione,
                                               unitaMisura=lav.unitaMisura, prezzoUnitario=lav.prezzoUnitario)
            returnList.append(newLav)

        return returnList

    def inserisciNote(numero_preventivo, revisione, nota):
        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                  tipologia='edile').update({'note': nota})

        PreventivoDBmodel.commit()

    def impostaDataUltimaModifica(numero_preventivo, revisione ):
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).update({'data_ultima_modifica': oggi})
        PreventivoEdile.commit()

    def revisionaPreventivo(numero_preventivo, revisione, dipendente_generatore):
        '''
         Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento,
         ne fa una copia ( compresa di lavorazioni e sottolavorazioni ) cambiando unicamente
         gli attributi "data", settata alla data odierna, e "dipendente_ultimaModifica", settato con lo username
         del dipendente che sta facendo la modifica.

        :param numero_preventivo, dipendente_ultimaModifica:
        :return:
        '''



        lastPrev = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='edile').first()

        ultimaRevisione = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, tipologia='edile').order_by(desc(PreventivoEdile.revisione)).first().revisione

        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        '''
        #se il preventivo viene modificato piu' volte lo stesso giorno non viene fatta alcuna copia "

        if str(now).split(' ')[0] == str(lastPrev.data):

            return (numero_preventivo, oggi)
        '''

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=lastPrev.intervento_commessa).first()

        preventivo = PreventivoEdile(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=commessa.intervento,
                                     indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune,
                                     revisione = ultimaRevisione+1, ricarico_generale=lastPrev.ricarico_generale)


        PreventivoDBmodel.addRowNoCommit(preventivo)
        PreventivoDBmodel.commit()

        PreventivoEdile.impostaDataUltimaModifica(numero_preventivo, ultimaRevisione+1)
        
        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, revisione=lastPrev.revisione).all()


        lavorazioni = PreventivoEdile.__duplicaLavorazioni__(lavorazioni)

        for lav in lavorazioni:
            lav.revisione = ultimaRevisione+1
            PreventivoDBmodel.addRowNoCommit(lav)

        PreventivoEdile.commit()

        sottolavorazioniCad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, revisione=lastPrev.revisione).all()

        sottolavorazioniCad = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniCad, 'cad')

        sottolavorazioniMl = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, revisione=lastPrev.revisione).all()

        sottolavorazioniMl = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMl, 'ml')

        sottolavorazioniMq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, revisione=lastPrev.revisione).all()

        sottolavorazioniMq = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMq, 'mq')

        sottolavorazioniMc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo, revisione=lastPrev.revisione).all()

        sottolavorazioniMc = PreventivoEdile.__duplicaSottolavorazioni__(sottolavorazioniMc, 'mc')


        sottolavorazioni = sottolavorazioniCad + sottolavorazioniMl + sottolavorazioniMc + sottolavorazioniMq

        for sottoLav in sottolavorazioni:
            sottoLav.revisione = ultimaRevisione+1
            PreventivoDBmodel.addRowNoCommit(sottoLav)

        PreventivoEdile.commit()

        return ( numero_preventivo, ultimaRevisione+1 )


    def __calcolcaOrdineSottolavorazione__( queryClass, numero_preventivo, revisione, ordine):
        ordine_sottolavorazione = 0

        aux = queryClass.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                   ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        while aux is not None:
            ordine_sottolavorazione += 1
            aux = queryClass.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                       ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        return ordine_sottolavorazione

    def __registraSottolavorazione__( numero_preventivo, revisione, ordine, ordine_sottolavorazione, unitaMisura,
                                        numero, prezzoBase, ricarico, larghezza=None, altezza=None, profondita=None):

        lavorazione = None
        if unitaMisura == 'cad':
            lavorazione = __SottolavorazioneCadPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione, numero=numero,
                                                             prezzoBase=prezzoBase, ricarico=ricarico)
        elif unitaMisura == 'ml':
            lavorazione = __SottolavorazioneMlPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza,
                                                           prezzoBase=prezzoBase, ricarico=ricarico)

        elif unitaMisura == 'mq':
            lavorazione = __SottolavorazioneMqPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza,
                                                           prezzoBase=prezzoBase, ricarico=ricarico )

        elif unitaMisura == 'mc':
            lavorazione = __SottolavorazioneMcPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita,
                                                           prezzoBase=prezzoBase, ricarico=ricarico)


        PreventivoDBmodel.addRow(lavorazione)


    def nuovaSottolavorazione(numero_preventivo, revisione, ordine):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first().unitaMisura
        prezzoBase = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first().prezzoUnitario
        ricaricoGenerale = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first().ricarico_generale

        if unitaMisura == 'cad':
            last_sottolav_cad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                  revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneCadPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                             ordine=ordine, ordine_sottolavorazione=last_sottolav_cad+1, numero=1, prezzoBase=prezzoBase,
                                                         ricarico=ricaricoGenerale)
        elif unitaMisura == 'ml':
            last_sottolav_ml = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMlPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_ml+1,
                                                         numero=1, larghezza=1, prezzoBase=prezzoBase, ricarico=ricaricoGenerale)

        elif unitaMisura == 'mq':
            last_sottolav_mq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMqPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mq+1,
                                                         numero=1, larghezza=1, altezza=1, prezzoBase=prezzoBase, ricarico=ricaricoGenerale)


        elif unitaMisura == 'mc':
            last_sottolav_mc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMcPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mc+1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1, prezzoBase=prezzoBase, ricarico=ricaricoGenerale)


    def registraLavorazione( numero_preventivo, revisione, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario,
                             numero, larghezza=None, altezza=None, profondita=None ):

        controlVar = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:
            lavorazione = __LavorazionePreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                    ordine=ordine, settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                                    unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario)
            PreventivoDBmodel.addRow(lavorazione)
        else: # se la lavorazione e' gia' presente registra la sottolavorazione

            if unitaMisura == 'cad':
                ordineSottolavorazione=PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneCadPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, revisione=revisione,
                                                                   ordine=ordine)
            elif unitaMisura == 'ml':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMlPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, revisione=revisione,
                                                                   ordine=ordine)

            elif unitaMisura == 'mq':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMqPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, revisione=revisione,
                                                                   ordine=ordine)

            elif unitaMisura == 'mc':
                ordineSottolavorazione =PreventivoEdile.__calcolcaOrdineSottolavorazione__(queryClass=__SottolavorazioneMcPreventivo__.query,
                                                                   numero_preventivo=numero_preventivo, revisione=revisione,
                                                                   ordine=ordine)

        ricaricoGenerale = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo,
                                                           revisione=revisione).first().ricarico_generale

        PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                     ordine=ordine, ordine_sottolavorazione=ordineSottolavorazione,
                                                     numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita,
                                                     prezzoBase=prezzoUnitario, ricarico=ricaricoGenerale)


    def eliminaLavorazione(numero_preventivo, revisione, ordine ):

        toDel = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first()

        # essendoci il vincolo d'integrita', eliminando una lavorazione si eliminano anche le relative sottolavorazioni
        PreventivoEdile.delRow(toDel)

        app.server.logger.info('fin qua ok esco')

    def eliminaSottolavorazione(numero_preventivo, revisione, ordine, ordine_sottolavorazione):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                          ordine=ordine).first().unitaMisura
        toDel = None

        if unitaMisura == 'cad':
            toDel = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()
        elif unitaMisura == 'ml':
            toDel = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mq':
            toDel = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        elif unitaMisura == 'mc':
            toDel = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                                      ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione).first()

        PreventivoEdile.delRow(toDel)


    def __settaOrdineNegativo__(lavorazione, queryClass):

        newOrdine = int(-lavorazione.ordine)

        queryClass.filter_by(numero_preventivo=lavorazione.numero_preventivo, revisione=lavorazione.revisione,
                                           ordine=lavorazione.ordine).update({'ordine': newOrdine})


    def iniziaRiordinoLavorazione(numero_preventivo, revisione):
        '''
           Prima di ogni riordino di voci all'interno del preventivo si prendono tutte le voci
           e si setta il loro campo "ordine" al negativo. Questo previene la situazione
           in cui cambiando il numero d'ordine di una voce ci si ritrovi in una situazione intermedia
           con due voci con lo stesso numero ( situazione d'errore in quanto ordine e' parte della chiave
           di una lavorazione) e, allo stesso tempo, di ricordare il vecchio ordine.
        '''

        lavPrev = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).all()
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


    def modificaOrdineLavorazione( modifica, numero_preventivo, revisione, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, revisione, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()

    def __settaOrdineSottolavorazioneNegativo__(sottolavorazione, queryClass):

        newOrdine = int(-sottolavorazione.ordine_sottolavorazione)

        queryClass.filter_by(numero_preventivo=sottolavorazione.numero_preventivo, revisione=sottolavorazione.revisione,
                             ordine=sottolavorazione.ordine,
                             ordine_sottolavorazione=sottolavorazione.ordine_sottolavorazione).update({'ordine_sottolavorazione': newOrdine})

    def iniziaRiordinoSottolavorazione(numero_preventivo, revisione, ordine, unitaMisura):
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


        sottolavPrev = queryClassSottolavorazione.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).all()
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



    def modificaOrdineSottolavorazione(numero_preventivo, revisione, ordine, old_ordine_sottolavorazione, unitaMisura,
                                       new_ordine_sottolavorazione):


        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                              ordine=ordine,
                                                              ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                { 'ordine_sottolavorazione': new_ordine_sottolavorazione })
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine,
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})



        PreventivoDBmodel.commit()
    def modificaSottolavorazione(modifica, numero_preventivo, revisione, ordine, ordine_sottolavorazione, unitaMisura):

        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione ).update(modifica)
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)


        PreventivoDBmodel.commit()

    def returnSingleBudget(numero_preventivo, revisione):
        '''
        si differenzia da returnSinglePreventivo() solo per il fatto che i totali sono calcolati basandosi
        sui prezzi per l'azienda presi dal prezzario (senza il ricarico per il cliente)
        '''

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).order_by(
                                                                __LavorazionePreventivo__.ordine).all()

        ordineSettori = []
        resultLav = []

        for lav in lavorazioni:
            sottolavorazioni = []

            if not ordineSettori.__contains__(lav.settore):
                ordineSettori.append(lav.settore)

            lavFromPrezzario = LavorazioneEdileDBmodel.query.filter_by(settore=lav.settore, tipologia_lavorazione=lav.tipologia_lavorazione).first()
            prezzoBase = float(lavFromPrezzario.prezzoMax)

            if lav.unitaMisura == 'cad':

                sottolavorazioni = __SottolavorazioneCadPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneCadPreventivo__.ordine_sottolavorazione).all()
                quantitaTotale = 0

                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += sottolav.numero
                    sommaPrezziSottolav += sottolav.numero * prezzoBase

                #prezzoTotale = quantitaTotale * lav.prezzoUnitario
                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'ml':
                sottolavorazioni = __SottolavorazioneMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMlPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza) * prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


            elif lav.unitaMisura == 'mq':
                sottolavorazioni = __SottolavorazioneMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMqPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza)*prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))



            elif lav.unitaMisura == 'mc':
                sottolavorazioni = __SottolavorazioneMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)*prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


        return ( ordineSettori, resultLav)

    def returnSinglePreventivo(numero_preventivo, revisione):

        '''

        :param: la chiave di un preventivo
        :return: una terna dalla forma: ( ordineSettori, resultLav, ricarico_generale )
            dove:
            - ordineSettori = lista ordinata di nomi di settore; ogni elemento appare una sola volta
                                e l'ordine riflette quello di comparsa nel relativo preventivo;
            - resultLav = lista di tuple; ogni tupla racchiude tutta l'informazione utile su una specifica
                            lavorazione nel preventivo.

            L'ordine di ogni tupla elemento di resultLav riflette quello di comparsa nel relativo preventivo;

            Ogni tupla elemento di resultLav ha la forma: (lavorazione, quantita, totale, sottolavorazioni).
        '''

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).order_by(
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
                                        revisione=revisione, ordine=lav.ordine).order_by(
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
                                        revisione=revisione, ordine=lav.ordine).order_by(
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
                                        revisione=revisione, ordine=lav.ordine).order_by(
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
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)
                    sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)*sottolav.prezzoBase

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

        ricarico_generale = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first().ricarico_generale

        return ( ordineSettori, resultLav, ricarico_generale )

    def returnLastPreventivoCliente(nome_cliente, cognome_cliente, indirizzo_cliente):

        last_prev = PreventivoEdile.query.filter_by(tipologia='edile', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                     indirizzo_cliente=indirizzo_cliente).order_by(desc(PreventivoEdile.revisione), desc(PreventivoEdile.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=last_prev.numero_preventivo, revisione=last_prev.revisione)


        return ( last_prev, ) + preventivoInfo

    def controlloModificaCommessa(numero_preventivo, vecchio_intervento_commessa,
                                    nuovo_intervento_commessa, indirizzo_commessa, comune_commessa):

        commessa_presente = __Commessa__.query.filter_by(numero_preventivo=numero_preventivo,
                                                         intervento=vecchio_intervento_commessa ).first()

        if commessa_presente is not None:

            commessa_presente.intervento = nuovo_intervento_commessa
            commessa_presente.indirizzo = indirizzo_commessa
            commessa_presente.comune = comune_commessa

            CommessaDBmodel.commit()

    def returnCommessa(numero_preventivo, intervento_commessa):

        return __Commessa__.query.filter_by(numero_preventivo=numero_preventivo, intervento=intervento_commessa).first()

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
                                                        PreventivoEdile.numero_preventivo, desc(PreventivoEdile.revisione)).all()

        returnList = []

        for prev in preventivi:
            returnList.append( ( prev, PreventivoEdile.returnSinglePreventivo(numero_preventivo=prev.numero_preventivo, revisione=prev.revisione)) )

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

    def chiudiPreventivo(numero_preventivo, revisione, sconto, tipologia, iva):

        preventivo= PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='edile').first()

        preventivo.stato=False
        preventivo.sconto_totale=sconto
        preventivo.tipologia_sconto_totale=tipologia
        preventivo.iva_totale = iva

        PreventivoEdile.commit()


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
                indexesToRet.append( indexesToRet[-1])
                indexesToRet[-2] = indexesToRet[-2]-1


            totLunghezzaUltimaPag = 0

            if len(indexesToRet) > 1:

                for lunghezza in grandezzaRighe[indexesToRet[-2]:indexesToRet[-1]]:
                    totLunghezzaUltimaPag+=lunghezza

                if totLunghezzaUltimaPag <= 4.5:
                    return ( indexesToRet, False )
                else:
                    return ( indexesToRet, True )
            else:

                return (indexesToRet, True)


        else:
            return ([], False)



    def stampaPreventivo(numero_preventivo, revisione, iva, tipoSconto, sconto, chiudiPreventivo, sumisura, budget=False ):
        '''

        :return: ritorna False se la commessa non e' compilata completamente e chiudiPreventivo == True
        '''


        preventivo = PreventivoEdile.query.filter_by(tipologia='edile', numero_preventivo=numero_preventivo,
                                                     revisione=revisione).first()

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=preventivo.intervento_commessa).first()

        if chiudiPreventivo:
            if commessa.intervento == '' or commessa.indirizzo == '' or commessa.comune == '':
                return False

        dipendente = DipendenteDBmodel.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        if not budget:
            infoPreventivo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=numero_preventivo, revisione=revisione)
        else:
            infoPreventivo = PreventivoEdile.returnSingleBudget(numero_preventivo=numero_preventivo, revisione=revisione)

        codicePrev = PreventivoEdile.calcolaCodicePreventivoNoObj(numero_preventivo, revisione)



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
                      '''

        if not budget:
            latexScript +=  '\\usepackage[top=1.7cm, bottom=5.5cm, left=2.6cm, right=2.6cm]{geometry}'
        else:
            latexScript += '\\usepackage[top=1.7cm, bottom=3cm, left=2.6cm, right=2.6cm]{geometry}'

        latexScript += '''
                        \\usepackage{fancyhdr}
                        \\pagestyle{fancy}
                        \\lhead{}
                        \\chead{} 
                      '''

        latexScript += '\\rhead{US' + codicePrev + 'E}'

        if not budget:
            latexScript += '''
                            \\cfoot{
                                    {\\normalsize
                                      \\begin{center}
                                      \\begin{tabular}{|L{105mm} | L{44mm}| }
                                      \\hline
                                      \\begin{spacing}{0.3}
                                        \\textbf{NOTE} \\newline
                                        \\hfill
                            '''
            if preventivo.note is not None:
                latexScript += '{\\centering '+preventivo.note+'}'
            else:
                latexScript += '{\\centering }'

            latexScript +=  '''
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
                                        \\textbf{UnionService Srl.} Via Roma n. 84 - 37060 Castel d'Azzano (VR) - Tel. +39 045 8521697 - Fax +39 045 8545123 \\\\
                                        Cell. +39 342 7663538 - C.F./P.iva 04240420234 - REA: VR-404097 \\\\ \\begin{flushright} \\thepage \\end{flushright}
                                    }
                            }
                            \\rfoot{}
                            \\renewcommand{\\headrulewidth}{0pt}
                        '''
        else:
            latexScript += '''
                            \\cfoot{
                                \\begin{spacing}{0.5}
                                {\\footnotesize
                                  \\textbf{UnionService Srl.} Via Roma n. 84 - 37060 Castel d'Azzano (VR) - Tel. +39 045 8521697 - Fax +39 045 8545123 \\\\
                                  Cell. +39 342 7663538 - C.F./P.iva 04240420234 - REA: VR-404097 \\\\ \\begin{flushright} \\thepage \\end{flushright}
                                }
                                \\end{spacing}
                            }
                            
                            \\rfoot{}
                            \\renewcommand{\\headrulewidth}{0pt}
                            \\renewcommand{\\footrulewidth}{0.4pt}
                         '''
                        
        latexScript +=  '''
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

        intervento_commessa = commessa.intervento
        indirizzo_commessa = commessa.indirizzo
        comune_commessa = commessa.comune

        if commessa.intervento == '':
            intervento_commessa = '-'
        if commessa.indirizzo == '':
            indirizzo_commessa = '-'
        if commessa.comune == '':
            comune_commessa = '-'


        latexScript += intervento_commessa.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                                  "\\'u").replace(
            "ì", "\\'i") + ' \\newline '


        latexScript += indirizzo_commessa.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace("ù",
                                                                                                                 "\\'u").replace(
            "ì", "\\'i") + ' \\newline ' + comune_commessa.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
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

        typeOfDoc = ''

        if not budget:
            typeOfDoc = 'Preventivo Edile'
        else:
            typeOfDoc = 'Budget'

        latexScript += '''
                          \\end{spacing}\\\\
                            \\hline
                          \\end{tabular}

                          \\begin{center}
                          \\begin{tabular}{|L{89mm} R{60mm}| }
                          \\hline
                          \\vspace{2.5mm}
                          \\begin{spacing}{0}
                        '''

        latexScript += '\\textbf{'+typeOfDoc+' - } \\textcolor{red}{revisione n.'+'{}'.format(revisione)+'}'

        latexScript +=  '''
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
                          
                        '''

        if not budget:
            latexScript +=  '''
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
                       '''

        headerLavorazioni = '''
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

        numPagine, lastPageAlone = PreventivoEdile.__calcolaLavorazioniPerPaginaPreventivo__(infoPreventivo[1])

        totalePreventivo = 0
        lastStartingIndex = 0
        indexActualPage = 0

        for numLastLav in numPagine:
            latexScript += headerLavorazioni

            for lav in infoPreventivo[1][lastStartingIndex:numLastLav+1]:

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

                latexScript += lav[0].nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                        "\\'o").replace(
                    "ù",
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
                latexScript += '{}'.format(round(lav[2]*100)/100)
                totalePreventivo += round(lav[2]*100)/100

                latexScript += '''
                                   \\end{spacing} \\\\
                                   \\hline
                                   %FINE RIGA

                                 '''


            latexScript +=  '\\end{tabular} \\\\'



            if indexActualPage+1 == len(numPagine):

                if not budget:

                    latexScript += '''
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
                        laberForSconto = "Sconto {}\%".format(sconto)
                    elif tipoSconto == 4:
                        totaleScontato = sconto
                        laberForSconto = "Totale scontato"

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

                    if lastPageAlone:
                        latexScript += '\\newpage'
                    else:
                        latexScript += '\\vspace{19mm}'

                else:
                    latexScript += '''
                                      \\noindent\\begin{tabular}{|L{133.1mm} |  L{16mm}| }
                                      \\hline
                                        \\vspace{2.5mm}
                                        \\begin{spacing}{0}
                                          \\textbf{Totale}
                                        \\end{spacing} &
                                      \\vspace{2.5mm}
                                      \\begin{spacing}{0}
                                        \\euro\\hfill
                                   '''

                    latexScript += '{}'.format(totalePreventivo)

                    latexScript += '''
                                      \\end{spacing}\\\\
                                      \\hline
                                      \\end{tabular}
                                      \\end{document}
                                   '''

            else:
                latexScript += '\\newpage'
                lastStartingIndex = numLastLav+1
                indexActualPage += 1

        if chiudiPreventivo:
            PagamentiCliente.generaPagamentoPerPreventivo(numero_preventivo)
            PagamentiCliente.modificaPagamento(numero_preventivo, {'totale_prev_edile': totaleConIva })

        if not budget:
            latexScript += '''
                              \\begin{figure}[!t]
                              \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                              \\end{figure}
                           '''

            latexScript += '''
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

        if chiudiPreventivo :
            PreventivoEdile.chiudiPreventivo(numero_preventivo, revisione, sconto, tipoSconto, iva)

        if not budget:
            with open('app/preventiviLatexDir/preventivoEdile-{}_{}.tex'.format(numero_preventivo, revisione), mode='w') as prova:
                prova.write(latexScript)
        else:
            with open('app/preventiviLatexDir/budgetEdile-{}_{}.tex'.format(numero_preventivo, revisione), mode='w') as prova:
                prova.write(latexScript)


        if not budget:
            os.system("cd app/preventiviLatexDir && pdflatex preventivoEdile-{}_{}.tex".format(numero_preventivo, revisione))
        else:
            os.system("cd app/preventiviLatexDir && pdflatex budgetEdile-{}_{}.tex".format(numero_preventivo, revisione))

        return True