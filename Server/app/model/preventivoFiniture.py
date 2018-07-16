from .db.preventivoDBmodel import PreventivoDBmodel
from .db.commessaDBmodel import CommessaDBmodel
from .db.prodottiPreventivoFiniture.prodottoPreventivoFinitureDBmodel import ProdottoPreventivoFinitureDBmodel
from .clienteAccolto import ClienteAccolto
from sqlalchemy import desc, func
import datetime
import app
import os




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
        self.tipologia = 'finiture'

class __Commessa__(CommessaDBmodel):
    def __init__(self, numero_preventivo, intervento, indirizzo, comune):
        self.numero_preventivo = numero_preventivo
        self.intervento = intervento
        self.indirizzo = indirizzo
        self.comune = comune

class PreventivoFiniture(PreventivoDBmodel):

    def __init__(self, numero_preventivo, data, nome_cliente, cognome_cliente,
                 indirizzo_cliente, dipendente_generatore, intervento_commessa, 
                 indirizzo_commessa, comune_commessa, dipendente_ultimaModifica=None, stato=True):

        commessa = __Commessa__(numero_preventivo=numero_preventivo, intervento=intervento_commessa,
                                indirizzo=indirizzo_commessa, comune=comune_commessa)
        __Commessa__.addRow(commessa)

        self.numero_preventivo = numero_preventivo
        self.data = data
        self.nome_cliente = nome_cliente
        self.cognome_cliente = cognome_cliente
        self.indirizzo_cliente = indirizzo_cliente
        self.dipendente_generatore = dipendente_generatore
        self.intervento_commessa_commessa = intervento_commessa
        self.tipologia='finiture'
        self.stato = stato

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
                           dipendente_generatore, numero_preventivo,
                           intervento_commessa, indirizzo_commessa, comune_commessa):


        if PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo).first() is not None:
            return PreventivoFiniture.modificaPreventivo(numero_preventivo)

        now = datetime.datetime.now()
        oggi = "{}/{}/{}".format(now.day, now.month, now.year)

        preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=nome_cliente,
                                     cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente,
                                     intervento_commessa=intervento_commessa, indirizzo_commessa=indirizzo_commessa,
                                     comune_commessa=comune_commessa,
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

        preventivi = PreventivoFiniture.query.filter_by( nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                        indirizzo_cliente=indirizzo_cliente ).order_by(PreventivoFiniture.numero_preventivo, desc(PreventivoFiniture.data)).all()
        listToReturn = []

        for preventivo in preventivi:
            listToReturn.append( (preventivo, PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=preventivo.numero_preventivo,
                                                                                          data=preventivo.data)) )

        return listToReturn

    def returnLastPreventivoCliente( nome_cliente, cognome_cliente, indirizzo_cliente ):
        last_prev = PreventivoFiniture.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente,
                                                    indirizzo_cliente=indirizzo_cliente).order_by(
            desc(PreventivoFiniture.data), desc(PreventivoFiniture.numero_preventivo)).first()

        if last_prev is None:
            return (None, [], [])

        preventivoInfo = PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=last_prev.numero_preventivo,
                                                                     data=last_prev.data)

        return (last_prev,) + preventivoInfo

    def modificaPreventivo(numero_preventivo):
        '''
                 Prende il preventivo che corrisponde al "numero_preventivo" passato come argomento e con la data
                 piu' recente, ne fa una copia cambiando unicamente
                 gli attributi "data", settata alla data odierna
        '''

        lastPrev = PreventivoFiniture.query.filter_by(numero_preventivo=numero_preventivo).order_by(
            desc(PreventivoFiniture.data)).first()
        now = datetime.datetime.now()
        oggi = "{}-{}-{}".format(now.year, now.month, now.day)

        # se il preventivo viene modificato piu' volte lo stesso giorno non viene fatta alcuna copia

        if str(now).split(' ')[0] != str(lastPrev.data):

            preventivo = PreventivoFiniture(numero_preventivo=numero_preventivo, data=oggi, nome_cliente=lastPrev.nome_cliente,
                                     cognome_cliente=lastPrev.cognome_cliente, indirizzo_cliente=lastPrev.indirizzo_cliente,
                                     dipendente_generatore=lastPrev.dipendente_generatore,
                                     intervento_commessa=lastPrev.intervento_commessa, indirizzo_commessa=lastPrev.indirizzo_commessa,
                                     comune_commessa=lastPrev.comune_commessa)

            PreventivoDBmodel.addRow(preventivo)

            prodotti = __ProdottoPreventivo__.query.filter_by(numero_preventivo=lastPrev.numero_preventivo,
                                                                    data=lastPrev.data).all()

            prodotti = PreventivoFiniture.__duplicaProdotti__(prodotti)

            for prodotto in prodotti:
                prodotto.data = oggi
                PreventivoDBmodel.addRowNoCommit(prodotto)

            PreventivoDBmodel.commit()

            return (numero_preventivo, oggi)

        else:
            return (numero_preventivo, lastPrev.data)


    def get_counter_preventivi_per_cliente(nome_cliente, cognome_cliente, indirizzo_cliente):
        q = PreventivoFiniture.query.filter_by(nome_cliente=nome_cliente, cognome_cliente=cognome_cliente, indirizzo_cliente=indirizzo_cliente)
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