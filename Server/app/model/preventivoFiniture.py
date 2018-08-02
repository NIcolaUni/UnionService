from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.dipendenteDBmodel import DipendenteDBmodel
from .db.prodottiPreventivoFiniture.prodottoPreventivoFinitureDBmodel import ProdottoPreventivoFinitureDBmodel
from .clienteAccolto import ClienteAccolto
from sqlalchemy import desc, func
import datetime
import app
import os
import math




class __ProdottoPreventivo__(ProdottoPreventivoFinitureDBmodel):
    def __init__(self, numero_preventivo, data, ordine, tipologia, nome_prodotto, modello, marchio, quantita,
                 unitaMisura, codice, diffCapitolato):

        self.numero_preventivo = numero_preventivo
        self.data = data
        self.ordine = ordine

        self.tipologia = tipologia
        self.nome_prodotto = nome_prodotto
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
                 indirizzo_commessa, comune_commessa, stato=True, note=None):


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



    def calcolaCodicePreventivo(self):
        # recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = self.data.year % 100

        # recupero le prime tre lettere del cognome del cliente
        dipendente = self.dipendente_generatore.split('_')[1][0:3].upper()

        return str(self.numero_preventivo) + dipendente + str(annoPreventivo)

    def calcolaCodicePreventivoNoObj(numero_preventivo, data):

        prev = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='finiture').first()

        #recupero le ultime due cifre dell'anno di creazione
        annoPreventivo = prev.data.year%100

        #recupero le prime tre lettere del cognome del cliente
        dipendente = prev.dipendente_generatore.split('_')[1][0:3].upper()

        return str(prev.numero_preventivo)+dipendente+str(annoPreventivo)

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

    def registraPreventivo_vecchiaCommessa( dipendente_generatore, numero_preventivo ):

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        oldPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo,
                                                     tipologia='finiture').order_by(desc(PreventivoFiniture.data)).first()

        if oldPrev is not None:
            return PreventivoFiniture.modificaPreventivo(numero_preventivo=numero_preventivo, data=oldPrev.data, dipendente_generatore=dipendente_generatore)



        prevEdile = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                          tipologia='edile').first()

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=prevEdile.intervento_commessa).first()

        app.server.logger.info('allora cominciamo piano {}'.format(commessa.intervento))
        preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=prevEdile.nome_cliente,
                                     cognome_cliente=prevEdile.cognome_cliente, indirizzo_cliente=prevEdile.indirizzo_cliente,
                                     intervento_commessa=commessa.intervento, indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune,
                                     dipendente_generatore=dipendente_generatore)

        PreventivoDBmodel.addRow(preventivo)

        return (numero_preventivo, oggi)

    def eliminaPreventivo(numero_preventivo, data):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data).first()

        PreventivoDBmodel.delRow(toDel)

    def registraProdotto(numero_preventivo, data, ordine, tipologia, nome_prodotto,
                            modello, marchio, quantita, unitaMisura, codice, diffCapitolato ):

        app.server.logger.info('ma perche\n\n\n')
        prodotto=__ProdottoPreventivo__(numero_preventivo=numero_preventivo, data=data, ordine=ordine,
                                        tipologia=tipologia, nome_prodotto=nome_prodotto, modello=modello, marchio=marchio,
                                        quantita=quantita, unitaMisura=unitaMisura, codice=codice, diffCapitolato=diffCapitolato)

        PreventivoDBmodel.addRow(prodotto)

    def __settaOrdineNegativo__(prodotto, queryClass):

        newOrdine = int(-prodotto.ordine)

        queryClass.filter_by(numero_preventivo=prodotto.numero_preventivo, data=prodotto.data,
                                           ordine=prodotto.ordine).update({'ordine': newOrdine})

    def iniziaRiordinoProdotti(numero_preventivo, data):

        prodottiPreventivo=__ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data)

        iniziaNuovoRiordino = True


        for prod in prodottiPreventivo:
            if prod.ordine < 0:
                iniziaNuovoRiordino = False

        if iniziaNuovoRiordino:
            for prod in prodottiPreventivo:
                PreventivoFiniture.__settaOrdineNegativo__(prod, __ProdottoPreventivo__.query)

            PreventivoDBmodel.commit()

    def modificaOrdineProdotto(numero_preventivo, data, oldOrdine, ordine):

        PreventivoFiniture.modificaProdotto(numero_preventivo=numero_preventivo, data=data, ordine=oldOrdine, modifica={'ordine': ordine})

        PreventivoFiniture.commit()

    def modificaProdotto(numero_preventivo, data, ordine, modifica):

        __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).update(modifica)

        PreventivoFiniture.commit()

    def eliminaProdotto(numero_preventivo, data, ordine):

        toDel = __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data, ordine=ordine).first()

        PreventivoFiniture.delRow(toDel)

    def returnProdottiPreventivo(numero_preventivo, data):

        prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=numero_preventivo, data=data).order_by(__ProdottoPreventivo__.ordine).all()

        tipologie = []

        for prodotto in prodotti:
            if prodotto.tipologia not in tipologie:
                tipologie.append(prodotto.tipologia)

        return ( tipologie, prodotti )

    def __duplicaProdotti__(prodotti):


        returnList = []
        for prodotto in prodotti:
            newProd = __ProdottoPreventivo__(numero_preventivo=prodotto.numero_preventivo, data=prodotto.data, ordine=prodotto.ordine,
                                        tipologia=prodotto.tipologia, nome_prodotto=prodotto.nome_prodotto, modello=prodotto.modello, marchio=prodotto.marchio,
                                        quantita=prodotto.quantita, unitaMisura=prodotto.unitaMisura, codice=prodotto.codice, diffCapitolato=prodotto.diffCapitolato)
            returnList.append(newProd)

        return returnList

    def returnAllPreventiviCliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        '''

        :return: ritorna una lista di tuple; ogni tupla ha la struttura: ( preventivo, ( tipologie, prodotti ) )
        '''

        preventivi = PreventivoFiniture.query.filter_by( tipologia='finiture', nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                        indirizzo_cliente=indirizzo_cliente ).order_by(PreventivoFiniture.numero_preventivo, desc(PreventivoFiniture.data)).all()
        listToReturn = []

        for preventivo in preventivi:
            listToReturn.append( (preventivo, PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=preventivo.numero_preventivo,
                                                                                          data=preventivo.data)) )

        return listToReturn

    def returnLastPreventivoCliente( nome_cliente, cognome_cliente, indirizzo_cliente ):
        last_prev = PreventivoFiniture.query.filter_by(tipologia='finiture',  nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                    indirizzo_cliente=indirizzo_cliente).order_by(
            desc(PreventivoFiniture.data), desc(PreventivoFiniture.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=last_prev.numero_preventivo,
                                                                     data=last_prev.data)

        return (last_prev,) + preventivoInfo

    def inserisciNote(numero_preventivo, data, nota):
        PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, data=data,
                                                  tipologia='finiture').update({'note': nota})

        PreventivoDBmodel.commit()

    def modificaPreventivo(numero_preventivo, data, dipendente_generatore):
        '''
                 Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
                 piu' recente, ne fa una copia cambiando unicamente
                 gli attributi "data", settata alla data odierna
        '''

        app.server.logger.info("inzizzissimo mod {} {} {}".format(numero_preventivo, data, dipendente_generatore))

        lastPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='finiture').first()

        app.server.logger.info("prima di commessa")

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo, intervento=lastPrev.intervento_commessa).first()

        app.server.logger.info("inziio mod")

        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        # se il preventivo viene modificato piu' volte lo stesso giorno non viene fatta alcuna copia

        if str(now).split(' ')[0] != str(lastPrev.data):

            preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=dipendente_generatore,
                                     intervento_commessa=commessa.intervento, indirizzo_commessa=commessa.indirizzo,
                                     comune_commessa=commessa.comune)

            PreventivoDBmodel.addRow(preventivo)

            app.server.logger.info("centro mod")

            prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo,
                                                                    data=lastPrev.data).all()

            prodotti = PreventivoFiniture.__duplicaProdotti__(prodotti)

            for prodotto in prodotti:
                prodotto.data = oggi
                PreventivoDBmodel.addRowNoCommit(prodotto)

            app.server.logger.info("fine mod")

            PreventivoDBmodel.commit()

            return (numero_preventivo, oggi)

        else:
            return (numero_preventivo, lastPrev.data)

    def eliminaPreventivo(numero_preventivo, data):

        toDel = PreventivoDBmodel.query.filter_by(numero_preventivo=numero_preventivo, data=data, tipologia='finiture').first()


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
            desc(PreventivoFiniture.data)).all()

        primo_giro = True

        for prev in preventivi:
            if primo_giro:
                primo_giro = False
                prev.stato = False
                PreventivoFiniture.commit()

            else:
                PreventivoFiniture.delRow(prev)

    def stampaPreventivo(numero_preventivo, data, iva, tipoSconto, sconto, chiudiPreventivo, sumisura):

        if chiudiPreventivo:
            PreventivoFiniture.chiudiPreventivo(numero_preventivo)



        preventivo = PreventivoFiniture.query.filter_by(tipologia='finiture', numero_preventivo=numero_preventivo,
                                                     data=data).first()

        dipendente = DipendenteDBmodel.query.filter_by(username=preventivo.dipendente_generatore).first()

        cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente,
                                                 indirizzo=preventivo.indirizzo_cliente).first()

        prodotti = PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=numero_preventivo, data=data)

        codicePrev = PreventivoFiniture.calcolaCodicePreventivoNoObj(numero_preventivo, data)

        commessa = CommessaDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                                   intervento=preventivo.intervento_commessa).first()

        contaProdotti = 0

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

        latexScript += '\\rhead{US' + codicePrev + 'F}'

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
                            \\textbf{Preventivo Finiture}
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
        app.server.logger.info('fine del header')
        totalePreventivo = 0

        for prod in prodotti[1]:
            contaProdotti += 1
            latexScript += '''
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''
            latexScript += '{}'.format(contaProdotti)

            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            latexScript += prod.nome_prodotto.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                          "\\'o").replace(
                "ù", "\\'u").replace("ì", "\\'i") + " - " + prod.modello.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                          "\\'o").replace(
                "ù", "\\'u").replace("ì", "\\'i") + " - " + prod.marchio.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                          "\\'o").replace(
                "ù", "\\'u").replace("ì", "\\'i")


            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += '{}'.format(prod.quantita)

            else:
                latexScript += '-'


            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                           '''

            if sumisura:
                latexScript += prod.unitaMisura

            else:
                latexScript += 'a corpo'


            latexScript += '''
                              \\end{spacing} &
                              \\vspace{2.5mm}
                              \\begin{spacing}{0}
                                \\euro\\hfill 
                            '''
            latexScript += '{}'.format(prod.diffCapitolato)
            totalePreventivo += prod.diffCapitolato

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

        with open('app/preventiviLatexDir/preventivoFiniture.tex', mode='w') as prova:
            prova.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex preventivoFiniture.tex")