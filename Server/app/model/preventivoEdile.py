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
from .contabilitaCantiere import ContabilitaCantiere
from .pagamentiCliente import PagamentiCliente
from .clienteAccolto import  ClienteAccolto
from .pdfGenerator import PdfGenerator
from sqlalchemy import desc, func
import datetime
import app




class __SottolavorazioneCadPreventivo__(SottolavorazioneCadDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione,
                    numero, prezzoBase, ricarico, nome_modificato):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico

        self.nome_modificato = nome_modificato


class __SottolavorazioneMlPreventivo__(SottolavorazioneMlDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione,
                    numero, larghezza, prezzoBase, ricarico, nome_modificato ):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.ordine_sottolavorazione = ordine_sottolavorazione
        self.tipologia = 'edile'

        self.numero = numero
        self.larghezza = larghezza

        self.prezzoBase = prezzoBase
        self.ricarico = ricarico

        self.nome_modificato = nome_modificato


class __SottolavorazioneMqPreventivo__(SottolavorazioneMqDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione,
                    numero, larghezza, altezza, prezzoBase, ricarico, nome_modificato ):
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

        self.nome_modificato =nome_modificato



class __SottolavorazioneMcPreventivo__(SottolavorazioneMcDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, ordine_sottolavorazione,
                    numero, larghezza, altezza, profondita, prezzoBase,
                        ricarico, nome_modificato ):
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

        self.nome_modificato = nome_modificato


class __LavorazionePreventivo__(LavorazionePreventivoDBmodel):
    def __init__(self,  numero_preventivo, revisione, ordine, settore,
                    tipologia_lavorazione, unitaMisura, prezzoUnitario,
                        assistenza, costo_assistenza, tipo_costo_assistenza, nome_modificato,
                            copia=False, ordine_lav_originale=0, settore_lav_copia=''):
        self.numero_preventivo=numero_preventivo
        self.revisione = revisione
        self.ordine = ordine
        self.tipologia = 'edile'

        self.settore = settore
        self.tipologia_lavorazione = tipologia_lavorazione
        self.nome_modificato = nome_modificato
        self.unitaMisura=unitaMisura
        self.prezzoUnitario=prezzoUnitario
        self.assistenza = assistenza
        self.costo_assistenza = costo_assistenza
        self.tipo_costo_assistenza = tipo_costo_assistenza

        self.copia=copia

        if copia:
            self.ordine_lav_originale=ordine_lav_originale
            self.settore_lav_copia=settore_lav_copia
        else:
            self.ordine_lav_originale = ordine
            self.settore_lav_copia = settore



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
                 stato=True, note='', revisione=1):

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
        self.ricarico_extra = 0



    def modificaPreventivo(numero_preventivo, revisione, modifica):

        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, tipologia="edile", revisione=revisione).update(modifica)
        PreventivoEdile.commit()

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
                                                                ricarico=sottolav.ricarico, nome_modificato=sottolav.nome_modificato)
                returnList.append(newSottolav)

        elif unitaMisura == 'ml':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMlPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               prezzoBase=sottolav.prezzoBase, ricarico=sottolav.ricarico, nome_modificato=sottolav.nome_modificato)
                returnList.append(newSottolav)

        elif unitaMisura == 'mq':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMqPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, prezzoBase=sottolav.prezzoBase,
                                                               ricarico=sottolav.ricarico, nome_modificato=sottolav.nome_modificato)
                returnList.append(newSottolav)

        elif unitaMisura == 'mc':
            for sottolav in sottolavorazioni:
                newSottolav = __SottolavorazioneMcPreventivo__(numero_preventivo=sottolav.numero_preventivo,
                                                               revisione=sottolav.revisione, ordine=sottolav.ordine,
                                                               ordine_sottolavorazione=sottolav.ordine_sottolavorazione,
                                                               numero=sottolav.numero, larghezza=sottolav.larghezza,
                                                               altezza=sottolav.altezza, profondita=sottolav.profondita,
                                                               prezzoBase=sottolav.prezzoBase, ricarico=sottolav.ricarico, nome_modificato=sottolav.nome_modificato)
                returnList.append(newSottolav)


        return returnList

    def __duplicaLavorazioni__(lavorazioni):

        returnList = []
        for lav in lavorazioni:
            newLav = __LavorazionePreventivo__(numero_preventivo=lav.numero_preventivo, revisione=lav.revisione,
                                               ordine=lav.ordine,
                                               settore=lav.settore, tipologia_lavorazione=lav.tipologia_lavorazione,
                                               unitaMisura=lav.unitaMisura, prezzoUnitario=lav.prezzoUnitario,
                                               assistenza=lav.assistenza, costo_assistenza=lav.costo_assistenza,
                                               tipo_costo_assistenza=lav.tipo_costo_assistenza,
                                               nome_modificato=lav.nome_modificato,
                                               copia=lav.copia, ordine_lav_originale=lav.ordine_lav_originale,
                                               settore_lav_copia=lav.settore_lav_copia)
            returnList.append(newLav)

        return returnList

    def inserisciNote(numero_preventivo, revisione, nota):
        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                  tipologia='edile').update({'note': nota})

        PreventivoDBmodel.commit()

    def impostaDataUltimaModifica(numero_preventivo, revisione ):
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)


        PreventivoEdile.modificaPreventivo(numero_preventivo=numero_preventivo,  revisione=revisione, modifica={'data_ultima_modifica': oggi})

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
                                        numero, prezzoBase, ricarico, nome_modificato,
                                            larghezza=None, altezza=None, profondita=None):

        lavorazione = None
        if unitaMisura == 'cad':
            lavorazione = __SottolavorazioneCadPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione, numero=numero,
                                                             prezzoBase=prezzoBase, ricarico=ricarico, nome_modificato=nome_modificato)
        elif unitaMisura == 'ml':
            lavorazione = __SottolavorazioneMlPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza,
                                                           prezzoBase=prezzoBase, ricarico=ricarico, nome_modificato=nome_modificato)

        elif unitaMisura == 'mq':
            lavorazione = __SottolavorazioneMqPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza,
                                                           prezzoBase=prezzoBase, ricarico=ricarico, nome_modificato=nome_modificato )

        elif unitaMisura == 'mc':
            lavorazione = __SottolavorazioneMcPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                           ordine=ordine,
                                                           ordine_sottolavorazione=ordine_sottolavorazione,
                                                           numero=numero, larghezza=larghezza, altezza=altezza, profondita=profondita,
                                                           prezzoBase=prezzoBase, ricarico=ricarico, nome_modificato=nome_modificato)


        PreventivoDBmodel.addRow(lavorazione)

    def modificaNomeSottolavorazione( numero_preventivo, revisione, ordine,
                                        unitaMisura, ordine_sottolavorazione, nome_modificato ):


        tipologia='edile'

        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                              tipologia=tipologia, ordine=ordine,
                                                              ordine_sottolavorazione=ordine_sottolavorazione).update({'nome_modificato':nome_modificato})
            PreventivoEdile.commit()

        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                              tipologia=tipologia, ordine=ordine,
                                                              ordine_sottolavorazione=ordine_sottolavorazione).update({'nome_modificato':nome_modificato})

            PreventivoEdile.commit()
        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                              tipologia=tipologia, ordine=ordine,
                                                              ordine_sottolavorazione=ordine_sottolavorazione).update({'nome_modificato':nome_modificato})
            PreventivoEdile.commit()
        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                              tipologia=tipologia, ordine=ordine,
                                                              ordine_sottolavorazione=ordine_sottolavorazione).update({'nome_modificato':nome_modificato})

            PreventivoEdile.commit()


    def nuovaSottolavorazione(numero_preventivo, revisione, ordine, nome_modificato):

        unitaMisura = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first().unitaMisura
        prezzoBase = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first().prezzoUnitario
        ricaricoGenerale = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first().ricarico_generale

        if unitaMisura == 'cad':

            try:
                last_sottolav_cad = __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                        revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneCadPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione
            except SyntaxError:
                last_sottolav_cad = -1



            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                             ordine=ordine, ordine_sottolavorazione=last_sottolav_cad+1, numero=1, prezzoBase=prezzoBase,
                                                         ricarico=ricaricoGenerale, nome_modificato=nome_modificato)
        elif unitaMisura == 'ml':

            try:
                last_sottolav_ml = __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMlPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione
            except AttributeError:
                last_sottolav_ml = -1

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_ml+1,
                                                         numero=1, larghezza=1, prezzoBase=prezzoBase,
                                                         ricarico=ricaricoGenerale, nome_modificato=nome_modificato)

        elif unitaMisura == 'mq':

            try:
                last_sottolav_mq = __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                    revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMqPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione
            except AttributeError:
                last_sottolav_mq = -1

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                                 ordine=ordine, ordine_sottolavorazione=last_sottolav_mq+1,
                                                                 numero=1, larghezza=1, altezza=1,
                                                                 prezzoBase=prezzoBase, ricarico=ricaricoGenerale, nome_modificato=nome_modificato)

        elif unitaMisura == 'mc':

            try:
                last_sottolav_mc = __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                                revisione=revisione, ordine=ordine).order_by( desc(__SottolavorazioneMcPreventivo__.ordine_sottolavorazione)).first().ordine_sottolavorazione

            except AttributeError:
                last_sottolav_mc= -1

            PreventivoEdile.__registraSottolavorazione__(numero_preventivo=numero_preventivo, revisione=revisione, unitaMisura=unitaMisura,
                                                         ordine=ordine, ordine_sottolavorazione=last_sottolav_mc+1,
                                                         numero=1, larghezza=1, altezza=1, profondita=1,
                                                         prezzoBase=prezzoBase, ricarico=ricaricoGenerale, nome_modificato=nome_modificato)

    def modificaPrezziClienteLavorazioni(numero_preventivo, revisione):

        preventivo = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first()
        lav_preventivo = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).all()
        lav_prezzario = LavorazioneEdileDBmodel.query.all()
        nuovoPrezzo = 0


        for lav in lav_preventivo:
            for lav_to_ctrl in lav_prezzario:
                if lav.settore == lav_to_ctrl.settore:
                    if lav.tipologia_lavorazione == lav_to_ctrl.tipologia_lavorazione:

                        nuovoPrezzo = lav_to_ctrl.prezzoMax+(lav_to_ctrl.prezzoMax*preventivo.ricarico_generale)/100;
                        nuovoPrezzo += nuovoPrezzo*preventivo.ricarico_extra/100;

            lav.prezzoUnitario = nuovoPrezzo

        PreventivoEdile.commit()

    def registraLavorazione( numero_preventivo, revisione, ordine, settore, tipologia_lavorazione, unitaMisura, prezzoUnitario,
                             assistenza, costo_assistenza, tipo_costo_assistenza,
                             numero, larghezza=None, altezza=None, profondita=None, copia=False,
                             ordine_lav_originale=0, settore_lav_copia=''):

        controlVar = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first()
        lavorazione = None
        ordineSottolavorazione = 0

        if controlVar is None:

            if not copia:
                lavorazione = __LavorazionePreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                        ordine=ordine, settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                                        unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario,
                                                        assistenza=assistenza, costo_assistenza=costo_assistenza, tipo_costo_assistenza=tipo_costo_assistenza,
                                                        nome_modificato=tipologia_lavorazione)
            else:
                lavorazione = __LavorazionePreventivo__(numero_preventivo=numero_preventivo, revisione=revisione,
                                                        ordine=ordine, settore=settore,
                                                        tipologia_lavorazione=tipologia_lavorazione,
                                                        unitaMisura=unitaMisura, prezzoUnitario=prezzoUnitario,
                                                        assistenza=assistenza, costo_assistenza=costo_assistenza,
                                                        tipo_costo_assistenza=tipo_costo_assistenza,
                                                        nome_modificato='', copia=True,
                                                        ordine_lav_originale=ordine_lav_originale,
                                                        settore_lav_copia=settore_lav_copia)

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
                                                     prezzoBase=prezzoUnitario, ricarico=ricaricoGenerale, nome_modificato=tipologia_lavorazione)


    def eliminaLavorazione(numero_preventivo, revisione, ordine ):

        toDel = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first()

        #verifico la presenza di eventuali lavorazioni copia e in caso modifico la loro referenza
        lav_copia = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                   copia=True, ordine_lav_originale=ordine).all()

        for lav in lav_copia:
            lav.ordine_lav_originale = lav.ordine # il commit viene poi fatto da delRow()


        # essendoci il vincolo d'integrita', eliminando una lavorazione si eliminano anche le relative sottolavorazioni
        PreventivoEdile.delRow(toDel)



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

        queryClass.filter_by(numero_preventivo=lavorazione.numero_preventivo, revisione=lavorazione.revisione, tipologia="edile",
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

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()


    def modificaLavorazione( modifica, numero_preventivo, revisione, ordine):

        __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                         ordine=ordine ).update(modifica)


        PreventivoDBmodel.commit()

    def __settaOrdineSottolavorazioneNegativo__(sottolavorazione, queryClass):

        newOrdine = int(-sottolavorazione.ordine_sottolavorazione)

        queryClass.filter_by(numero_preventivo=sottolavorazione.numero_preventivo, revisione=sottolavorazione.revisione,
                             ordine=sottolavorazione.ordine, tipologia="edile",
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
                                                              ordine=ordine, tipologia="edile",
                                                              ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                { 'ordine_sottolavorazione': new_ordine_sottolavorazione })
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine, tipologia="edile",
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine, tipologia="edile",
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                             ordine=ordine, tipologia="edile",
                                                             ordine_sottolavorazione=old_ordine_sottolavorazione).update(
                {'ordine_sottolavorazione': new_ordine_sottolavorazione})



        PreventivoDBmodel.commit()
    def modificaSottolavorazione(modifica, numero_preventivo, revisione, ordine, ordine_sottolavorazione, unitaMisura):

        if unitaMisura == 'cad':
            __SottolavorazioneCadPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                             ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione ).update(modifica)
        elif unitaMisura == 'ml':
            __SottolavorazioneMlPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mq':
            __SottolavorazioneMqPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)

        elif unitaMisura == 'mc':
            __SottolavorazioneMcPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia="edile",
                                            ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione  ).update(modifica)


        PreventivoDBmodel.commit()

    def returnSingleBudget(numero_preventivo, revisione):
        '''
        si differenzia da returnSinglePreventivo() solo per il fatto che i totali sono calcolati basandosi
        sui prezzi per l'azienda presi dal prezzario (senza il ricarico per il cliente)
        '''

        ordineSettori = []
        resultLav = []

        secondo_ricarico = PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first().ricarico_extra

        lavorazioni = __LavorazionePreventivo__.query.filter_by(numero_preventivo=numero_preventivo,
                                                                revisione=revisione).order_by(
            __LavorazionePreventivo__.ordine).all()

        for lav in lavorazioni:
            sottolavorazioni = []
            costo_assistenza = lav.costo_assistenza

            if lav.copia:
                if not ordineSettori.__contains__(lav.settore_lav_copia):
                    ordineSettori.append(lav.settore_lav_copia)
            else:
                if not ordineSettori.__contains__(lav.settore):
                    ordineSettori.append(lav.settore)

            if lav.unitaMisura == 'cad':

                sottolavorazioni = __SottolavorazioneCadPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneCadPreventivo__.ordine_sottolavorazione).all()
                quantitaTotale = 0
                sommaPrezziSottolav = 0
                prezzoBase = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += sottolav.numero

                    prezzoBase = sottolav.prezzoBase*100/(100+secondo_ricarico)
                    prezzoBase = prezzoBase*100/(100+sottolav.ricarico)

                if lav.tipo_costo_assistenza:
                    prezzoCliente = prezzoBase + (prezzoBase * costo_assistenza / 100)
                    sommaPrezziSottolav += quantitaTotale * prezzoCliente
                else:
                    sommaPrezziSottolav += quantitaTotale * (prezzoBase + costo_assistenza)

                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))


            elif lav.unitaMisura == 'ml':
                sottolavorazioni = __SottolavorazioneMlPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMlPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0
                prezzoBase = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza)

                    prezzoBase = sottolav.prezzoBase * 100 / (100 + secondo_ricarico)
                    prezzoBase = prezzoBase * 100 / (100 + sottolav.ricarico)

                if lav.tipo_costo_assistenza:
                    prezzoCliente = prezzoBase + (prezzoBase * costo_assistenza / 100)
                    sommaPrezziSottolav += quantitaTotale * prezzoCliente
                else:
                    sommaPrezziSottolav += quantitaTotale * (prezzoBase + costo_assistenza)


                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'mq':
                sottolavorazioni = __SottolavorazioneMqPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMqPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0
                prezzoBase = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza)

                    prezzoBase = sottolav.prezzoBase * 100 / (100 + secondo_ricarico)
                    prezzoBase = prezzoBase * 100 / (100 + sottolav.ricarico)

                if lav.tipo_costo_assistenza:
                    prezzoCliente = prezzoBase + (prezzoBase * costo_assistenza / 100)
                    sommaPrezziSottolav += quantitaTotale * prezzoCliente
                else:
                    sommaPrezziSottolav += quantitaTotale * (prezzoBase + costo_assistenza)


                prezzoTotale = sommaPrezziSottolav

                resultLav.append((lav, quantitaTotale, prezzoTotale, sottolavorazioni))

            elif lav.unitaMisura == 'mc':
                sottolavorazioni = __SottolavorazioneMcPreventivo__.query.filter_by(
                                        numero_preventivo=numero_preventivo,
                                        revisione=revisione, ordine=lav.ordine).order_by(
                                        __SottolavorazioneMcPreventivo__.ordine_sottolavorazione).all()

                quantitaTotale = 0
                sommaPrezziSottolav = 0
                prezzoBase = 0

                for sottolav in sottolavorazioni:
                    quantitaTotale += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)
                    prezzoBase = sottolav.prezzoBase * 100 / (100 + secondo_ricarico)
                    prezzoBase = prezzoBase * 100 / (100 + sottolav.ricarico)

                if lav.tipo_costo_assistenza:
                    prezzoCliente = prezzoBase + (prezzoBase * costo_assistenza / 100)
                    sommaPrezziSottolav +=  quantitaTotale * prezzoCliente
                else:
                    sommaPrezziSottolav +=  quantitaTotale * (prezzoBase + costo_assistenza)


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
            costo_assistenza = lav.costo_assistenza

            if lav.copia:
                if not ordineSettori.__contains__(lav.settore_lav_copia):
                    ordineSettori.append(lav.settore_lav_copia)
            else:
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
                    if lav.tipo_costo_assistenza:
                        prezzoCliente = sottolav.prezzoBase+(sottolav.prezzoBase*costo_assistenza/100)
                        sommaPrezziSottolav += sottolav.numero * prezzoCliente
                    else:
                        sommaPrezziSottolav += sottolav.numero * ( sottolav.prezzoBase+costo_assistenza )

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

                    if lav.tipo_costo_assistenza:
                        prezzoCliente = sottolav.prezzoBase + (sottolav.prezzoBase * costo_assistenza / 100)
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza) * prezzoCliente
                    else:
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza) * ( sottolav.prezzoBase+costo_assistenza )

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

                    if lav.tipo_costo_assistenza:
                        prezzoCliente = sottolav.prezzoBase + (sottolav.prezzoBase * costo_assistenza / 100)
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza) * prezzoCliente

                    else:
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza)*( sottolav.prezzoBase+costo_assistenza )

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

                    if lav.tipo_costo_assistenza:
                        prezzoCliente = sottolav.prezzoBase + (sottolav.prezzoBase * costo_assistenza / 100)
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita) * prezzoCliente
                    else:
                        sommaPrezziSottolav += (sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita)*( sottolav.prezzoBase+costo_assistenza )

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
        app.server.logger.info('entro chiudiPrevetivo() ')

        preventivo= PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='edile').first()

        preventivo.stato=False
        preventivo.sconto_totale=sconto
        preventivo.tipologia_sconto_totale=tipologia
        preventivo.iva_totale = iva

        PreventivoEdile.commit()

        prevBudget = PreventivoEdile.returnSingleBudget(numero_preventivo=numero_preventivo, revisione=revisione)

        for lav in prevBudget[1]:
            ContabilitaCantiere.creaContabilita(numero_preventivo=numero_preventivo, revisione=revisione,
                                                tipologia='edile', ordine_lav=lav[0].ordine,
                                                budget=lav[2], costi_effettivi=0, fattura=0, nome_lav=lav[0].nome_modificato )

    def impostaBudgetImprevisti(numero_preventivo, revisione, budget):

        PreventivoEdile.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).update({
            'budget_imprevisti' : budget
        })

        ContabilitaCantiere.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).update({
            'budget_imprevisti' : budget,
            'costi_effettivi_budget_imprevisti' : budget,
            'fattura_budget_imprevisti' : 0
        })

        PreventivoEdile.commit()


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

        totaleConIva = PdfGenerator.generaPdfPreventivoLavorazioni(edile=True, preventivo=preventivo, codicePrev=codicePrev,
                                                        commessa=commessa, dipendente=dipendente,
                                                        cliente=cliente, infoPreventivo=infoPreventivo, iva=iva,
                                                            tipoSconto=tipoSconto, sconto=sconto,
                                                                sumisura=sumisura, budget=budget)

        if chiudiPreventivo:
            PagamentiCliente.generaPagamentoPerPreventivo(numero_preventivo)
            PagamentiCliente.modificaPagamento(numero_preventivo, {'totale_prev_edile': totaleConIva })
            PreventivoEdile.chiudiPreventivo(numero_preventivo, revisione, sconto, tipoSconto, iva)


        #Se si sta chiudendo il preventivo devo generare anche "l'altro" tipo di preventivo poichè questa
        #altrimenti non si potrebbe più chiamare la corrente funzione.
        if not budget and chiudiPreventivo:
            PreventivoEdile.stampaPreventivo(numero_preventivo=numero_preventivo, revisione=revisione, iva=iva,
                                                tipoSconto=tipoSconto, sconto=sconto,
                                                    chiudiPreventivo=False, sumisura=(not sumisura), budget=False)




        return True