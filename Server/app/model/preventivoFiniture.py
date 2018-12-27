from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.dipendenteDBmodel import DipendenteDBmodel
from .db.prodottiPreventivoFiniture.prodottoPreventivoFinitureDBmodel import ProdottoPreventivoFinitureDBmodel
from .clienteAccolto import ClienteAccolto
from .pagamentiCliente import  PagamentiCliente
from sqlalchemy import desc, func
import datetime
import app
import os
import math




class __ProdottoPreventivo__(ProdottoPreventivoFinitureDBmodel):
    def __init__(self, numero_preventivo, revisione, ordine, tipologia, nome_prodotto, modello, marchio, quantita,
                 unitaMisura, codice, diffCapitolato):

        self.numero_preventivo = numero_preventivo
        self.revisione = revisione
        self.ordine = ordine

        self.tipologia = tipologia
        self.nome_prodotto = nome_prodotto
        self.nome_modificato = nome_prodotto
        self.unitaMisura = unitaMisura
        self.modello = modello
        self.marchio = marchio
        self.quantita = quantita
        self.codice = codice
        self.diffCapitolato = diffCapitolato
        self.tipologia_preventivo = 'finiture'

class __Commessa__(CommessaDBmodel):
    def __init__(self, numero_preventivo, intervento, indirizzo, comune):
        self.numero_preventivo = numero_preventivo
        self.intervento = intervento
        self.indirizzo = indirizzo
        self.comune = comune

class PreventivoFiniture(PreventivoDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, intervento_commessa, 
                 indirizzo_commessa, comune_commessa, stato=True, note=None, revisione=1):


        oldCommessa = __Commessa__.query.filter_by(numero_preventivo=numero_preventivo, intervento=intervento_commessa).first()

        if oldCommessa is None:
            commessa = __Commessa__(numero_preventivo=numero_preventivo, intervento=intervento_commessa,
                                    indirizzo=indirizzo_commessa, comune=comune_commessa)
            __Commessa__.addRow(commessa)

        self.numero_preventivo = numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.intervento_commessa = intervento_commessa
        self.tipologia='finiture'
        self.stato = stato
        self.note=note
        self.revisione=revisione



    def calcolaCodicePreventivo(self):
        # recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year % 100

        # recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo) + dipendente + str(annoPreventivo)

    def calcolaCodicePreventivoNoObj(numero_preventivo, revisione):

        prev = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='finiture').first()

        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = prev.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = prev.dipendente_generatore.split('_')[1][0:3].upper()

        return str(prev.numero_preventivo)+dipendente+str(annoPreventivo)
    '''
    def registraPreventivo_nuovaCommessa( nome_cliente, cognome_cliente, indirizzo_cliente,
                           dipendente_generatore, intervento_commessa, indirizzo_commessa, comune_commessa):

        youngerPrev = PreventivoDBmodel.query.order_by(desc(PreventivoDBmodel.numero_preventivo)).first()
        lastNumPrev = 99

        # se ci sono gia' preventivi registrati prende il numero_preventivo del piu' recente
        if youngerPrev is not None:
            lastNumPrev = youngerPrev.numero_preventivo

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoFiniture(numero_preventivo=lastNumPrev+1, data=oggi,
                                        nome_cliente=nome_cliente,
                                        cognome_cliente=cognome_cliente,
                                        indirizzo_cliente=indirizzo_cliente,
                                        intervento_commessa=intervento_commessa,
                                        indirizzo_commessa=indirizzo_commessa,
                                        comune_commessa=comune_commessa,
                                        dipendente_generatore=dipendente_generatore)

        PreventivoDBmodel.addRow(preventivo)

        return (lastNumPrev+1, oggi)
    '''

    def registraPreventivo_vecchiaCommessa( dipendente_generatore, numero_preventivo ):

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        oldPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo,
                                                     tipologia='finiture').order_by(desc(PreventivoFiniture.revisione)).first()

        if oldPrev is not None:
            return PreventivoFiniture.revisionaPreventivo(numero_preventivo=numero_preventivo, revisone=oldPrev.revisione, dipendente_generatore=dipendente_generatore)



        prevEdile = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                          tipologia='edile').first()

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=prevEdile.intervento_commessa).first()


        preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=prevEdile.nome_cliente,
                                     cognome_cliente=prevEdile.cognome_cliente, indirizzo_cliente=prevEdile.indirizzo_cliente,
                                     intervento_commessa=commessa.intervento, indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune,
                                     dipendente_generatore=dipendente_generatore, revisione=1)

        PreventivoDBmodel.addRow(preventivo)

        return (numero_preventivo, 1)

    def eliminaPreventivo(numero_preventivo, revisione):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).first()

        PreventivoDBmodel.delRow(toDel)

    def registraProdotto(numero_preventivo, revisione, ordine, tipologia, nome_prodotto,
                            modello, marchio, quantita, unitaMisura, codice, diffCapitolato ):


        prodotto=__ProdottoPreventivo__(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine,
                                        tipologia=tipologia, nome_prodotto=nome_prodotto, modello=modello, marchio=marchio,
                                        quantita=quantita, unitaMisura=unitaMisura, codice=codice, diffCapitolato=diffCapitolato)

        PreventivoDBmodel.addRow(prodotto)

    def __settaOrdineNegativo__(prodotto, queryClass):

        newOrdine = int(-prodotto.ordine)

        queryClass.filter_by(numero_preventivo=prodotto.numero_preventivo, revisione=prodotto.revisione,
                                           ordine=prodotto.ordine).update({'ordine': newOrdine})

    def iniziaRiordinoProdotti(numero_preventivo, revisione):

        prodottiPreventivo=__ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione)

        iniziaNuovoRiordino = True


        for prod in prodottiPreventivo:
            if prod.ordine < 0:
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            for prod in prodottiPreventivo:
                PreventivoFiniture.__settaOrdineNegativo__(prod, __ProdottoPreventivo__.query)

            PreventivoDBmodel.commit()

    def modificaOrdineProdotto(numero_preventivo, revisione, oldOrdine, ordine):

        PreventivoFiniture.modificaProdotto(numero_preventivo=numero_preventivo, revisione=revisione, ordine=oldOrdine, modifica={'ordine': ordine})

        PreventivoFiniture.commit()

    def modificaProdotto(numero_preventivo, revisione, ordine, modifica):

        __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).update(modifica)

        PreventivoFiniture.commit()


    def eliminaProdotto(numero_preventivo, revisione, ordine):

        toDel = __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, ordine=ordine).first()

        PreventivoFiniture.delRow(toDel)

    def returnProdottiPreventivo(numero_preventivo, revisione):

        prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).order_by(__ProdottoPreventivo__.ordine).all()

        tipologie = []

        for prodotto in prodotti:
            if prodotto.tipologia not in tipologie:
                tipologie.append(prodotto.tipologia)

        return ( tipologie, prodotti )

    def __duplicaProdotti__(prodotti):


        returnList = []
        for prodotto in prodotti:
            newProd = __ProdottoPreventivo__(numero_preventivo=prodotto.numero_preventivo, revisione=prodotto.revisione, ordine=prodotto.ordine,
                                        tipologia=prodotto.tipologia, nome_prodotto=prodotto.nome_prodotto, modello=prodotto.modello, marchio=prodotto.marchio,
                                        quantita=prodotto.quantita, unitaMisura=prodotto.unitaMisura, codice=prodotto.codice, diffCapitolato=prodotto.diffCapitolato)
            returnList.append(newProd)

        return returnList

    def returnAllPreventiviCliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        '''

        :return: ritorna una lista di tuple; ogni tupla ha la struttura: ( preventivo, ( tipologie, prodotti ) )
        '''

        preventivi = PreventivoFiniture.query.filter_by( tipologia='finiture', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                        indirizzo_cliente=indirizzo_cliente ).order_by(PreventivoFiniture.numero_preventivo, desc(PreventivoFiniture.revisione)).all()
        listToReturn = []

        for preventivo in preventivi:
            listToReturn.append( (preventivo, PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=preventivo.numero_preventivo,
                                                                                          revisione=preventivo.revisione)) )

        return listToReturn

    def returnLastPreventivoCliente( nome_cliente, cognome_cliente, indirizzo_cliente ):
        last_prev = PreventivoFiniture.query.filter_by(tipologia='finiture',  nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                    indirizzo_cliente=indirizzo_cliente).order_by(
            desc(PreventivoFiniture.revisione), desc(PreventivoFiniture.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=last_prev.numero_preventivo,
                                                                     revisione=last_prev.revisione)

        return (last_prev,) + preventivoInfo

    def inserisciNote(numero_preventivo, revisione, nota):
        PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                  tipologia='finiture').update({'note': nota})

        PreventivoDBmodel.commit()

    def revisionaPreventivo(numero_preventivo, revisione, dipendente_generatore):
        '''
                 Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
                 piu' recente, ne fa una copia cambiando unicamente
                 gli attributi "data", settata alla data odierna
        '''



        lastPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='finiture').first()
        ultimaRevisione = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo,
                                                          tipologia='finiture').order_by(
            desc(PreventivoFiniture.revisione)).first().revisione

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo, intervento=lastPrev.intervento_commessa).first()



        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)


        preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                 cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                 dipendente_generatore=dipendente_generatore,
                                 intervento_commessa=commessa.intervento, indirizzo_commessa=commessa.indirizzo,
                                 comune_commessa=commessa.comune, revisione=ultimaRevisione+1)

        PreventivoDBmodel.addRow(preventivo)



        prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo,
                                                                data=lastPrev.data).all()

        prodotti = PreventivoFiniture.__duplicaProdotti__(prodotti)

        for prodotto in prodotti:
            prodotto.revisione = ultimaRevisione+1
            PreventivoDBmodel.addRowNoCommit(prodotto)

        PreventivoDBmodel.commit()

        return (numero_preventivo, ultimaRevisione+1)



    def eliminaPreventivo(numero_preventivo, revisione):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione, tipologia='finiture').first()


        PreventivoDBmodel.delRow(toDel)

    def get_counter_preventivi_per_cliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        q = PreventivoFiniture.query.filter_by(tipologia='finiture',  nome_cliente=nome_cliente, cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def get_counter_preventivi_per_numero(numero_preventivo):
        q = PreventivoFiniture.query.filter_by(tipologia='finiture', numero_preventivo=numero_preventivo)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def chiudiPreventivo(numero_preventivo):

        preventivi = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, tipologia='finiture').order_by(
            desc(PreventivoFiniture.revisione)).all()

        primo_giro = True

        for prev in preventivi:
            if primo_giro:
                primo_giro = False
                prev.stato = False
                PreventivoFiniture.commit()

            else:
                PreventivoFiniture.delRow(prev)

    def modificaNomeProdotto(numero_preventivo, revisione, ordine, nuovo_nome):

        __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                                  tipologia_preventivo='finiture', ordine=ordine).update({'nome_modificato': nuovo_nome})

        PreventivoDBmodel.commit()


    def __calcolaIndiceLastProdottoPagineIntermedie__(startingIndex, grandezzaRighe):

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

    def __calcoraIndiceLastProdottoPrimaPagina__(grandezzaRighe):
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

    def __calcolaProdottiPerPaginaPreventivo__(prodotti):
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
        for prod in prodotti:
            numeroRighe = int(len( prod[0].nome_modificato )/50)
            resto = len( prod[0].nome_modificato )%50

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

            index, continua = PreventivoFiniture.__calcoraIndiceLastProdottoPrimaPagina__(grandezzaRighe)


            indexesToRet.append(index)

            while continua and index+1 < len(grandezzaRighe):

                index, continua = PreventivoFiniture.__calcolaIndiceLastProdottoPagineIntermedie__(index, grandezzaRighe[index+1:len(grandezzaRighe)])
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

    def returnSinglePreventivo(numero_preventivo, revisione):

        '''

        :param: la chiave di un preventivo
        :return: una coppia dalla forma: ( ordineSettori, resultProd )
            dove:
            - ordineSettori = lista ordinata di nomi di settore; ogni elemento appare una sola volta
                                e l'ordine riflette quello di comparsa nel relativo preventivo;
            - resultLav = lista di tuple; ogni tupla racchiude tutta l'informazione utile su uno specifico
                            prodotto nel preventivo.

        '''

        prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).order_by(
                                                                __ProdottoPreventivo__.ordine).all()

        ordineTipologie = []
        resultProd = []

        for prodotto in prodotti:

            if not ordineTipologie.__contains__(prodotto.tipologia):
                ordineTipologie.append(prodotto.tipologia)

            prezzoTotale = prodotto.quantita*prodotto.diffCapitolato

            resultProd.append((prodotto,  prezzoTotale))

        return (ordineTipologie, resultProd)

    def stampaPreventivo(numero_preventivo, revisione, chiudiPreventivo):
        if chiudiPreventivo:
            PreventivoFiniture.chiudiPreventivo(numero_preventivo)

        preventivo = PreventivoFiniture.query.filter_by(tipologia='finiture', numero_preventivo=numero_preventivo,
                                                     revisione=revisione).first()

        dipendente = DipendenteDBmodel.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()


        infoPreventivo = PreventivoFiniture.returnSinglePreventivo(numero_preventivo=numero_preventivo, revisione=revisione)


        codicePrev = PreventivoFiniture.calcolaCodicePreventivoNoObj(numero_preventivo, revisione)

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
                        '''

        latexScript += '\\usepackage[top=1.7cm, bottom=4.5cm, left=2.6cm, right=2.6cm]{geometry}'


        latexScript += '''
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
                          '''
        if preventivo.note is not None:
            latexScript += '{\\centering ' + preventivo.note + '}'
        else:
            latexScript += '{\\centering }'

        latexScript += '''
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


        latexScript += '''
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

        typeOfDoc = ''


        typeOfDoc = 'Preventivo Scelta Finiture'


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

        latexScript += '''
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
                         '''

        headerProdotti = '''
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
                              \\textbf{Diff. Capitolato}
                            \\end{spacing} \\\\
                            \\hline
                            %FINE HEADER
                         '''

        numPagine, lastPageAlone = PreventivoFiniture.__calcolaProdottiPerPaginaPreventivo__(infoPreventivo[1])

        totalePreventivo = 0
        lastStartingIndex = 0
        indexActualPage = 0

        for numLastLav in numPagine:
            latexScript += headerProdotti

            for prod in infoPreventivo[1][lastStartingIndex:numLastLav + 1]:

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

                marchio = prod[0].marchio.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                "\\'o").replace(
                    "ù",
                    "\\'u").replace(
                    "ì", "\\'i")

                modello = prod[0].modello.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                "\\'o").replace(
                    "ù",
                    "\\'u").replace(
                    "ì", "\\'i")

                nome= prod[0].nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                        "\\'o").replace(
                    "ù",
                    "\\'u").replace(
                    "ì", "\\'i")

                latexScript += marchio + ' - ' + modello + ' - ' + prod[0].codice + '\\newline '
                latexScript += nome

                latexScript += '''
                                     \\end{spacing} &
                                     \\vspace{2.5mm}
                                     \\begin{spacing}{0}
                                  '''


                latexScript += '{}'.format(prod[0].quantita)


                latexScript += '''
                                     \\end{spacing} &
                                     \\vspace{2.5mm}
                                     \\begin{spacing}{0}
                                  '''

                latexScript += prod[0].unitaMisura


                latexScript += '''
                                     \\end{spacing} &
                                     \\vspace{2.5mm}
                                     \\begin{spacing}{0}
                                       \\euro\\hfill 
                                   '''
                latexScript += '{}'.format(round(prod[1]*100)/100)
                totalePreventivo += prod[1]

                latexScript += '''
                                     \\end{spacing} \\\\
                                     \\hline
                                     %FINE RIGA
    
                                   '''

            latexScript += '\\end{tabular} \\\\'

            if indexActualPage + 1 == len(numPagine):
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

                latexScript += '{}'.format(round(totalePreventivo*100)/100)

                latexScript += '''
                                                        \\end{spacing}\\\\
                                                        \\hline
                                                        \\end{tabular}
                               '''


                if lastPageAlone:
                    latexScript += '\\newpage'
                else:
                    latexScript += '\\vspace{19mm}'



            else:
                latexScript += '\\newpage'
                lastStartingIndex = numLastLav + 1
                indexActualPage += 1

        if chiudiPreventivo:
            PagamentiCliente.generaPagamentoPerPreventivo(numero_preventivo)
            PagamentiCliente.modificaPagamento(numero_preventivo, {'totale_prev_finiture': round(totalePreventivo*100)/100 })

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

        with open('app/preventiviLatexDir/preventivoFiniture-{}_{}.tex'.format(numero_preventivo, revisione), mode='w') as prova:
            prova.write(latexScript)


        os.system("cd app/preventiviLatexDir && pdflatex preventivoFiniture-{}_{}.tex".format(numero_preventivo, revisione))
