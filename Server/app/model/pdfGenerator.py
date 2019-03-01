from .db.lavorazioneEdileDBmodel import LavorazioneEdileDBmodel
import math
import datetime
import os
import app

class PdfGenerator():

    def __init__(self):
        pass


    def __controllaSeNuovoSettorePreventivoSuMisura__(lavorazioneCorrente, settoreCorrente):
        '''
            utilizzata in __costruisciCorpoPreventivoSuMisura__() per semplificare la lettura
            e il debugging
        '''

        latexScript = ''
        nuovoSettore = settoreCorrente

        if (lavorazioneCorrente.settore != settoreCorrente and not lavorazioneCorrente.copia) or (
                lavorazioneCorrente.settore_lav_copia != settoreCorrente and lavorazioneCorrente.copia):
            # se non e' stata già aggiunta, inserisco la riga col titolo del settore di lavorazione

            if lavorazioneCorrente.copia:
                nuovoSettore = lavorazioneCorrente.settore_lav_copia
            else:
                nuovoSettore = lavorazioneCorrente.settore

            latexScript += '''
                                \\multicolumn{9}{ | L{124.5mm} |}{
                                \\vspace{2.5mm}
                                \\begin{spacing}{0}
                                \\textbf{
                           '''
            latexScript += '{}'.format(nuovoSettore)

            latexScript += '''                    
                                }
                                \\end{spacing}
                                } \\\\
                                \hline
                            '''

        return (latexScript, nuovoSettore)

    def __aggiungiRigaSottolavorazionePreventivoSuMisura__(sottolav, lavorazioneCorrente, budget, ricaricoExtra):
        '''
            utilizzata in __costruisciCorpoPreventivoSuMisura__() per semplificare la lettura
            e il debugging
        '''

        latexScript = ''
        startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
        endCellCode = '\\end{spacing} &'

        # la riga vuota in finalCellCode è necessaria altrimenti si rischia che nella stringa finale
        # il codice venga messo sulla stessa riga e, essendo che finalCellCode termina con un commento Latex,
        # si rischia che una parte del codice successivamente inserito venga considerato commento

        finalCellCode = '''
                        \\end{spacing} \\\\ \\hline %FINE RIGA

                        '''
        euroCellCode = '\\euro\\hfill '

        if sottolav.ordine_sottolavorazione == 0:
            latexScript += startCellCode
            latexScript += '{}'.format(lavorazioneCorrente.ordine)
            latexScript += endCellCode
        else:
            latexScript += startCellCode
            latexScript += endCellCode

        latexScript += startCellCode
        '''
        latexScript += sottolav.nome_modificato[0:100].replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                  "\\'o").replace(
            "ù",
            "\\'u").replace(
            "ì", "\\'i")

        if len(sottolav.nome_modificato) >= 100:
            latexScript+= '...'
            
        '''

        latexScript += sottolav.nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                         "\\'o").replace(
            "ù",
            "\\'u").replace(
            "ì", "\\'i")

        latexScript += endCellCode


        numSottolav = '-'
        larghezzaSottolav = '-'
        altezzaSottolav = '-'
        profonditaSottolav = '-'

        quantitaSottolavorazione = 0

        if lavorazioneCorrente.unitaMisura == 'cad':
            numSottolav = '{}'.format(sottolav.numero)

            quantitaSottolavorazione = sottolav.numero

        elif lavorazioneCorrente.unitaMisura == 'ml':
            numSottolav = '{}'.format(sottolav.numero)
            larghezzaSottolav = '{}'.format(sottolav.larghezza)

            quantitaSottolavorazione = sottolav.numero * sottolav.larghezza

        elif lavorazioneCorrente.unitaMisura == 'mq':
            numSottolav = '{}'.format(sottolav.numero)
            larghezzaSottolav = '{}'.format(sottolav.larghezza)
            altezzaSottolav = '{}'.format(sottolav.altezza)

            quantitaSottolavorazione = sottolav.numero * sottolav.larghezza * sottolav.altezza

        elif lavorazioneCorrente.unitaMisura == 'mc':
            numSottolav = '{}'.format(sottolav.numero)
            larghezzaSottolav = '{}'.format(sottolav.larghezza)
            altezzaSottolav = '{}'.format(sottolav.altezza)
            profonditaSottolav = '{}'.format(sottolav.profondita)

            quantitaSottolavorazione = sottolav.numero * sottolav.larghezza * sottolav.altezza * sottolav.profondita

        prezzoBaseSottolav = sottolav.prezzoBase

        if budget:
            prezzoBaseSottolav = sottolav.prezzoBase
            primoRicarico = sottolav.ricarico
            secondoRicarico = ricaricoExtra

            prezzoBaseSottolav = prezzoBaseSottolav * 100 / (100 + secondoRicarico)
            prezzoBaseSottolav = prezzoBaseSottolav * 100 / (100 + primoRicarico)

        if lavorazioneCorrente.tipo_costo_assistenza:
            prezzoBaseSottolav += (prezzoBaseSottolav * lavorazioneCorrente.costo_assistenza / 100)
        else:
            prezzoBaseSottolav += lavorazioneCorrente.costo_assistenza

        totaleSottolavorazione = quantitaSottolavorazione * prezzoBaseSottolav

        latexScript += startCellCode
        latexScript += '{}'.format(numSottolav)
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{}'.format(larghezzaSottolav)
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{}'.format(altezzaSottolav)
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{}'.format(profonditaSottolav)
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{}'.format(quantitaSottolavorazione)
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += lavorazioneCorrente.unitaMisura
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{} {}'.format(euroCellCode, round(totaleSottolavorazione * 100) / 100)
        latexScript += finalCellCode

        return latexScript

    def __aggiungiRigaAssistenzaPreventivoSuMisura__(lavorazioneCorrente):

        '''
            utilizzata in __costruisciCorpoPreventivoSuMisura__() per semplificare la lettura
            e il debugging
        '''

        latexScript = ''

        if lavorazioneCorrente.assistenza != 'No assistenza':
            startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
            endCellCode = '\\end{spacing} &'

            # la riga vuota in finalCellCode è necessaria altrimenti si rischia che nella stringa finale
            # il codice venga messo sulla stessa riga e, essendo che finalCellCode termina con un commento Latex,
            # si rischia che una parte del codice successivamente inserito venga considerato commento

            finalCellCode = '''
                            \\end{spacing} \\\\ \\hline %FINE RIGA
    
                            '''
            euroCellCode = '\\euro\\hfill '

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += 'Assistenza: \\newline {}'.format(
                lavorazioneCorrente.assistenza.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace(
                    "ù",
                    "\\'u").replace(
                    "ì", "\\'i"))
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += startCellCode
            latexScript += endCellCode

            if lavorazioneCorrente.assistenza != 'No assistenza':
                if lavorazioneCorrente.tipo_costo_assistenza:
                    latexScript += startCellCode
                    latexScript += '{} \%'.format(lavorazioneCorrente.costo_assistenza)
                    latexScript += finalCellCode
                else:
                    latexScript += startCellCode
                    latexScript += '{} {}'.format(euroCellCode, lavorazioneCorrente.costo_assistenza)
                    latexScript += finalCellCode
            else:
                latexScript += startCellCode
                latexScript += '-'
                latexScript += finalCellCode

        return latexScript

    def __concludiPreventivoSuMisura__(budget, budget_imprevisti, totalePreventivo, tipoSconto, sconto, iva,
                                       lastPageAlone):
        '''
            utilizzata in __costruisciCorpoPreventivoSuMisura__() per semplificare la lettura
            e il debugging
        '''

        euroCellCode = '\\euro\\hfill '
        latexScript = ''


        if not budget:

            if iva != 0:
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
            elif iva == 0 and tipoSconto != 1:
                latexScript += '''
                                           \\noindent\\begin{tabular}{|L{108.5mm} | L{8mm} | L{8mm} |  L{16mm}| }
                                           \\hline
                                           \\multicolumn{3}{ | L{133.1mm} | }{
                                             \\vspace{2.5mm}
                                             \\begin{spacing}{0}
                                               \\textbf{Totale imponibile}
                                             \\end{spacing}
                                           } &
                                           \\vspace{2.5mm}
                                           \\begin{spacing}{0}
                                             \\euro\\hfill
                                        '''
            else:
                latexScript += '''
                                           \\noindent\\begin{tabular}{| L{10mm} |  L{86mm} | L{12mm} | L{12mm} | L{16mm} | }
                                           \\hline
                                           \\multicolumn{4}{ | L{133.1mm} | }{
                                             \\vspace{2.5mm}
                                             \\begin{spacing}{0}
                                               \\textbf{Totale imponibile}
                                             \\end{spacing}
                                           } &
                                           \\vspace{2.5mm}
                                           \\begin{spacing}{0}
                                             \\euro\\hfill
                                        '''

            if iva != 0:

                latexScript += '{}'.format(totalePreventivo)

                latexScript += '''
                                   \\end{spacing}\\\\
                                   \\hline
                                '''

                totaleScontato = totalePreventivo
                laberForSconto = ""

                if tipoSconto == 2:
                    totaleScontato -= sconto
                    laberForSconto = "Sconto \\newline {} -{}".format(euroCellCode, sconto)
                elif tipoSconto == 3:
                    totaleScontato -= totalePreventivo * sconto / 100
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

                # se non c'è l'iva
            else:

                latexScript += '{}'.format(totalePreventivo)

                latexScript += '''
                                               \\end{spacing}\\\\
                                               \\hline
                                            '''

                totaleScontato = totalePreventivo
                laberForSconto = ""

                if tipoSconto == 2:
                    totaleScontato -= sconto
                    laberForSconto = "Sconto \\newline {} -{}".format(euroCellCode, sconto)
                elif tipoSconto == 3:
                    totaleScontato -= totalePreventivo * sconto / 100
                    laberForSconto = "Sconto {}\%".format(sconto)
                elif tipoSconto == 4:
                    totaleScontato = sconto
                    laberForSconto = "Totale scontato"

                totaleConIva = totaleScontato

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
                               \\end{tabular}
                               '''

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
                           '''

            latexScript += '''
                           \\noindent\\begin{tabular}{|L{133.1mm} |  L{16mm}| }
                           \\hline
                           \\vspace{2.5mm}
                           \\begin{spacing}{0}
                                \\textbf{Budget imprevisti}
                           \\end{spacing} &
                           \\vspace{2.5mm}
                           \\begin{spacing}{0}
                            \\euro\\hfill
                           '''

            latexScript += '{}'.format(budget_imprevisti)

            latexScript += '''
                              \\end{spacing}\\\\
                              \\hline
                              \\end{tabular}
                           '''
            latexScript += '\\end{document}'


        if lastPageAlone:
            latexScript += '\\newpage'
        else:
            latexScript += '\\vspace{19mm}'

        return latexScript

    def __aggiungiRigaFornituraPosaPreventivoSuMisura__(lavorazioneCorrente):

        '''
             utilizzata in __costruisciCorpoPreventivoSuMisura__() per semplificare la lettura
             e il debugging
         '''

        startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
        endCellCode = '\\end{spacing} &'
        euroCellCode = '\\euro\\hfill '
        finalCellCode = '''
                        \\end{spacing} \\\\ \\hline %FINE RIGA

                        '''

        lavFromPrezzario = LavorazioneEdileDBmodel.query.filter_by(
            tipologia_lavorazione=lavorazioneCorrente.tipologia_lavorazione,
            settore=lavorazioneCorrente.settore).first()

        latexScript = ''


        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += 'Fornitura:'
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        if lavFromPrezzario.fornitura == 0:
            latexScript += '-'
        else:
            latexScript += '{} {}'.format(euroCellCode, lavFromPrezzario.fornitura)
        latexScript += finalCellCode


        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += 'Posa:'
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += endCellCode

        latexScript += startCellCode
        if lavFromPrezzario.posa == 0:
            latexScript += '-'
        else:
            latexScript += '{} {}'.format(euroCellCode, lavFromPrezzario.posa)
        latexScript += finalCellCode

        return latexScript

    def __costruisciCorpoPreventivoSuMisura__(infoPrev, numPagine, lastPageAlone, headerLavorazioni, budget,
                                              tipoSconto, sconto, iva, preventivo):

        '''
            La logica di tale funzione è simile a quella della relativa a corpo
            con la differenza sostanziale che qua vengono considerate come singole lavorazioni
            le sottolavorazioni e quindi anche tutti i ragionamenti relativi vengono fatti sulle
            sottolavorazioni piuttosto che sulle lavorazioni
        '''


        latexScript = ''
        totalePreventivo = 0
        indexLastLav = 0
        indexLastSottolav = 0

        interrompiCicloLavorazioni = False
        counterSottolavInserite = 0

        settoreCorrente = ''
        contaPagine = 0

        for numLastSottolav in numPagine:
            contaPagine += 1
            latexScript += headerLavorazioni

            for lav in infoPrev[indexLastLav:len(infoPrev)]:

                for sottolav in lav[3][indexLastSottolav:len(lav[3])]:
                    if counterSottolavInserite <= numLastSottolav:

                        result = PdfGenerator.__controllaSeNuovoSettorePreventivoSuMisura__(lavorazioneCorrente=lav[0],
                                                                                            settoreCorrente=settoreCorrente)

                        latexScript += result[0]
                        settoreCorrente = result[1]

                        latexScript += PdfGenerator.__aggiungiRigaSottolavorazionePreventivoSuMisura__(
                            sottolav=sottolav, lavorazioneCorrente=lav[0],
                            budget=budget, ricaricoExtra=preventivo.ricarico_extra)

                        counterSottolavInserite += 1
                        indexLastSottolav += 1

                    else:
                        interrompiCicloLavorazioni = True
                        break

                if interrompiCicloLavorazioni:
                    interrompiCicloLavorazioni = False
                    break

                latexScript += PdfGenerator.__aggiungiRigaAssistenzaPreventivoSuMisura__(lavorazioneCorrente=lav[0])
                if budget:
                    latexScript += PdfGenerator.__aggiungiRigaFornituraPosaPreventivoSuMisura__(lavorazioneCorrente=lav[0])

                indexLastLav += 1
                indexLastSottolav = 0
                totalePreventivo += round(lav[2] * 100) / 100

            if( contaPagine < len(numPagine) ):
                # cambia pagina
                latexScript += '\\end{tabular} \\\\'
                latexScript += ' \\newpage'
                latexScript += '''
                                \\begin{figure}[!t]
                                \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                                \\end{figure}
                                '''
            else:
                latexScript += '\\end{tabular} \\\\'


        # parte finale preventivo
        latexScript += PdfGenerator.__concludiPreventivoSuMisura__(budget=budget, budget_imprevisti=preventivo.budget_imprevisti,
                                                       totalePreventivo=totalePreventivo, tipoSconto=tipoSconto,
                                                       sconto=sconto, iva=iva, lastPageAlone=lastPageAlone)

        return latexScript

    def __aggiungiRigaLavorazionePreventivoACorpo__(lavorazioneCorrente, totaleLavorazione):
        '''
            utilizzata in __costruisciCorpoPreventivoACorpo__() per semplificare la lettura
            e il debugging
        '''


        startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
        endCellCode = '\\end{spacing} &'
        finalCellCode = '''
                         \\end{spacing} \\\\ \\hline %FINE RIGA

                         '''
        euroCellCode = '\\euro\\hfill '

        latexScript = ''

        latexScript += startCellCode
        latexScript += '{}'.format(lavorazioneCorrente.ordine)
        latexScript += endCellCode
        latexScript += startCellCode
        latexScript += lavorazioneCorrente.nome_modificato.replace("à", "\\'a").replace("è", "\\'e").replace("ò",
                                                                                                             "\\'o").replace(
            "ù",
            "\\'u").replace(
            "ì", "\\'i")
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '-'
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += 'a corpo'
        latexScript += endCellCode

        latexScript += startCellCode
        latexScript += '{} {}'.format(euroCellCode, (round(totaleLavorazione * 100) / 100))
        latexScript += finalCellCode

        return latexScript

    def __aggiungiRigaAssistenzaPreventivoACorpo__(lavorazioneCorrente):
        '''
            utilizzata in __costruisciCorpoPreventivoACorpo__() per semplificare la lettura
            e il debugging
        '''


        startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
        endCellCode = '\\end{spacing} &'
        latexScript = ''

        if lavorazioneCorrente.assistenza != 'No assistenza':
            latexScript += startCellCode
            latexScript += endCellCode

            latexScript += '\\multicolumn{4}{  L{124.5mm} |}{'
            latexScript += startCellCode
            latexScript += 'Assistenza: \\newline {}'.format(
                lavorazioneCorrente.assistenza.replace("à", "\\'a").replace("è", "\\'e").replace("ò", "\\'o").replace(
                    "ù",
                    "\\'u").replace(
                    "ì", "\\'i"))

            latexScript += '\end{spacing}'

            latexScript += '''
                            } \\\\ \\hline %FINE RIGA

                           '''

        return latexScript

    def __controllaSeNuovoSettorePreventivoACorpo__(lavorazioneCorrente, settoreCorrente):
        '''
            utilizzata in __costruisciCorpoPreventivoACorpo__() per semplificare la lettura
            e il debugging
        '''

        latexScript = ''
        nuovoSettore = settoreCorrente

        if (lavorazioneCorrente.settore != settoreCorrente and not lavorazioneCorrente.copia) or (
                lavorazioneCorrente.settore_lav_copia != settoreCorrente and lavorazioneCorrente.copia):

            if lavorazioneCorrente.copia:
                nuovoSettore = lavorazioneCorrente.settore_lav_copia
            else:
                nuovoSettore = lavorazioneCorrente.settore

            latexScript += '''
                                 \\multicolumn{5}{ | L{124.5mm} |}{
                                 \\vspace{2.5mm}
                                 \\begin{spacing}{0}
                                 \\textbf{
                            '''

            latexScript += '{}'.format(nuovoSettore)

            latexScript += '''                    
                                 }
                                 \\end{spacing}
                                 } \\\\
                                 \hline
                            '''

        return (latexScript, nuovoSettore)

    def __concludiPreventivoACorpo__(totalePreventivo, lastPageAlone, tipoSconto, sconto, iva):
        '''
            utilizzata in __costruisciCorpoPreventivoACorpo__() per semplificare la lettura
            e il debugging
        '''


        euroCellCode = '\\euro\\hfill '
        latexScript = ''

        if iva != 0:
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
        elif iva ==0 and tipoSconto != 1 :
            latexScript += '''
                               \\noindent\\begin{tabular}{|L{108.5mm} | L{8mm} | L{8mm} |  L{16mm}| }
                               \\hline
                               \\multicolumn{3}{ | L{133.1mm} | }{
                                 \\vspace{2.5mm}
                                 \\begin{spacing}{0}
                                   \\textbf{Totale imponibile}
                                 \\end{spacing}
                               } &
                               \\vspace{2.5mm}
                               \\begin{spacing}{0}
                                 \\euro\\hfill
                            '''
        else:
            latexScript += '''
                               \\noindent\\begin{tabular}{| L{10mm} |  L{86mm} | L{12mm} | L{12mm} | L{16mm} | }
                               \\hline
                               \\multicolumn{4}{ | L{133.1mm} | }{
                                 \\vspace{2.5mm}
                                 \\begin{spacing}{0}
                                   \\textbf{Totale imponibile}
                                 \\end{spacing}
                               } &
                               \\vspace{2.5mm}
                               \\begin{spacing}{0}
                                 \\euro\\hfill
                            '''


        if iva != 0:



            latexScript += '{}'.format(totalePreventivo)

            latexScript += '''
                               \\end{spacing}\\\\
                               \\hline
                            '''

            totaleScontato = totalePreventivo
            laberForSconto = ""

            if tipoSconto == 2:
                totaleScontato -= sconto
                laberForSconto = "Sconto \\newline {} -{}".format(euroCellCode, sconto)
            elif tipoSconto == 3:
                totaleScontato -= totalePreventivo * sconto / 100
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


            #se non c'è l'iva
        else:

            latexScript += '{}'.format(totalePreventivo)

            latexScript += '''
                                           \\end{spacing}\\\\
                                           \\hline
                                        '''

            totaleScontato = totalePreventivo
            laberForSconto = ""

            if tipoSconto == 2:
                totaleScontato -= sconto
                laberForSconto = "Sconto \\newline {} -{}".format(euroCellCode, sconto)
            elif tipoSconto == 3:
                totaleScontato -= totalePreventivo * sconto / 100
                laberForSconto = "Sconto {}\%".format(sconto)
            elif tipoSconto == 4:
                totaleScontato = sconto
                laberForSconto = "Totale scontato"

            totaleConIva = totaleScontato


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
                           \\end{tabular}
                           '''


        if lastPageAlone:
            latexScript += '\\newpage'
        else:
            latexScript += '\\vspace{19mm}'


        return ( latexScript, totaleConIva )

    def __costruisciCorpoPreventivoACorpo__(infoPrev, numPagine, lastPageAlone, headerLavorazioni, tipoSconto, sconto,
                                            iva):

        latexScript = ''
        totalePreventivo = 0
        lastStartingIndex = 0
        indexActualPage = 0
        contaLavorazioni = 0

        settoreCorrente = ''

        for numLastLav in numPagine:
            latexScript += headerLavorazioni
            #numLastLav = numLastLav-1

           # app.server.logger.info('\n\nda {} a {}'.format(lastStartingIndex, numLastLav+1))

            for lav in infoPrev[lastStartingIndex:numLastLav +1]:
                result = PdfGenerator.__controllaSeNuovoSettorePreventivoACorpo__(lavorazioneCorrente=lav[0],
                                                                                           settoreCorrente=settoreCorrente)
                latexScript += result[0]
                settoreCorrente = result[1]
                contaLavorazioni += 1

                latexScript += PdfGenerator.__aggiungiRigaLavorazionePreventivoACorpo__(lavorazioneCorrente=lav[0],
                                                                                           totaleLavorazione=lav[2])

                totalePreventivo += round(lav[2] * 100) / 100

                latexScript += PdfGenerator.__aggiungiRigaAssistenzaPreventivoACorpo__(lavorazioneCorrente=lav[0])

            latexScript += '\\end{tabular} \\\\'

            if indexActualPage + 1 == len(numPagine):

                 scriptToAppend, totalePreventivo = PdfGenerator.__concludiPreventivoACorpo__(totalePreventivo=totalePreventivo,
                                                                            lastPageAlone=lastPageAlone,
                                                                            tipoSconto=tipoSconto, sconto=sconto,
                                                                            iva=iva)
                 latexScript += scriptToAppend
            else:
                # nuova pagina
                latexScript += '\\newpage'
                latexScript += '''
                                 \\begin{figure}[!t]
                                 \\includegraphics[width=15.8cm, height=3cm]{intestazioneAlta2.jpg}
                                 \\end{figure}
                                '''
                lastStartingIndex = numLastLav + 1
                indexActualPage += 1


        return latexScript, totalePreventivo

    def __generaIntestazionePreventivoEdile__(budget, preventivo, codicePrev, commessa, dipendente, cliente):


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
            latexScript += '\\usepackage[top=1.7cm, bottom=5.5cm, left=2.6cm, right=2.6cm]{geometry}'
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

        latexScript += '\\newline -'

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

        if preventivo.revisione == 1:
            latexScript += '\\textbf{' + typeOfDoc + '}'
        else:
            latexScript += '\\textbf{' + typeOfDoc + ' - } \\textcolor{red}{revisione n.' + '{}'.format(preventivo.revisione-1) + '}'

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

                                '''

        if not budget:
            latexScript += '''
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

        return latexScript

    def __generaHederTabellaLavorazioni__( sumisura, budget ):
        startCellCode = '\\vspace{2.5mm}\\begin{spacing}{0}'
        endCellCode = '\\end{spacing} &'
        finalCellCode = '''
                        \\end{spacing} \\\\ \\hline %FINE RIGA

                        '''

        headerLavorazioni = ''

        if sumisura or budget:
            headerLavorazioni = '''
                                      \\noindent\\begin{tabular}{ | L{6.1mm} |  L{52.4mm} |  L{7mm} | L{7mm} | L{7mm} | L{7mm} | L{8mm} | L{8mm} | L{16mm} |   }
                                      \\hline
                                '''
            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Pos.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Descrizione}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{N}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{L}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{H}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{P}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Qnt.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{U.M.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Importo}'
            headerLavorazioni += finalCellCode


        else:
            headerLavorazioni = '''
                                  \\noindent\\begin{tabular}{ | L{10mm} |  L{86mm} | L{12mm} | L{12mm} | L{16mm} | }
                                  \\hline
                                '''

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Pos.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Descrizione}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Qnt.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{U.M.}'
            headerLavorazioni += endCellCode

            headerLavorazioni += startCellCode
            headerLavorazioni += '\\textbf{Importo}'
            headerLavorazioni += finalCellCode

        return headerLavorazioni

    def __calcolaIndiceLastLavorazionePagineIntermedie__(startingIndex, grandezzaRighe, sconto):

        '''

        sconto e' un booleano:
        :return: un array dove in prima posizione c'è l'indice dell'ultima lavorazione
                da inserire nella pagina corrente e in seconda posizione un booleano
                indicante se il totale e' contenuto nella pagina corrente o finisce
                nella pagina successiva
        '''

        index = startingIndex
        tmpGrandezzaRighe = 0
        limitePaginaConTotale = 0
        limitePaginaSenzaTotale = 19.8#20.7#19.8#17.1

        if sconto:
            limitePaginaConTotale = 13.5
        else:
            limitePaginaConTotale = 14.4

        #limitePaginaConTotale -= 0.9


        #if grandezzaRighe[index] > limitePaginaSenzaTotale:
        #    app.server.logger.info('\n\nmmm {}'.format(len(grandezzaRighe)))
        #    return [index+1, True]

        for lunghezza in grandezzaRighe:

            tmpGrandezzaRighe += lunghezza
            tmpGrandezzaRighe = round(tmpGrandezzaRighe*100)/100

            if tmpGrandezzaRighe < limitePaginaSenzaTotale:
                index += 1
            elif tmpGrandezzaRighe > limitePaginaSenzaTotale:
              #  tmpGrandezzaRighe -= lunghezza
              #  tmpGrandezzaRighe = round(tmpGrandezzaRighe * 100) / 100
                index -= 1
                break
            else:
                break

        if tmpGrandezzaRighe < limitePaginaConTotale:
            return [index, False]
        elif tmpGrandezzaRighe == limitePaginaConTotale:
            return [index, True]
        else:
            return [index, True]

    def __calcoraIndiceLastLavorazionePrimaPagina__(grandezzaRighe, sconto ):

        '''

        sconto e' un booleano:
        :return: un array dove in prima posizione c'è l'indice dell'ultima lavorazione
                da inserire nella pagina corrente e in seconda posizione un booleano
                indicante se il totale e' contenuto nella pagina corrente o finisce
                nella pagina successiva
        '''
        index = 0
        tmpGrandezzaRighe = 0
        limitePaginaConTotale = 0
        limitePaginaSenzaTotale = 10.8#9.9

        if sconto:
            limitePaginaConTotale =  7.2#7.2
        else:
            limitePaginaConTotale =  9#8.1


        for lunghezza in grandezzaRighe:

            tmpGrandezzaRighe += lunghezza
            tmpGrandezzaRighe = round(tmpGrandezzaRighe*100)/100

            if tmpGrandezzaRighe < limitePaginaSenzaTotale:
                index += 1
            elif tmpGrandezzaRighe > limitePaginaSenzaTotale:

                #tmpGrandezzaRighe -= lunghezza
                #tmpGrandezzaRighe = round(tmpGrandezzaRighe * 100) / 100
                index -= 1
                break;
            else:
                break


        if tmpGrandezzaRighe < limitePaginaConTotale:
            return [index, False]
        elif tmpGrandezzaRighe == limitePaginaConTotale:
            return [index, True]
        else:
            return  [index, True]



    def __calcolaGrandezzaRigaInCm__(descrizione, caratteriPerRiga):
        '''
        questa funzione calcola approssimativamente la grandezza di una riga nel
        preventivo basandosi sul numero di caratteri componenti la voce descrizione.
        Per cercare di essere il più precisi possibili si considera che se diamo una
        dimensione astratta di 1 ad un carattare minuscolo al relativo carattere masiuscolo
        daremo una dimensione di 0.67.

        :return: ritorna un float indicante la grandezza in cm che occupa la riga
        '''

        lunghezzaRigaCm = 0

        numeroCaratteriDescrizione = 0

        for carattere in descrizione:
            if carattere.islower():
                numeroCaratteriDescrizione += 1
            else:
                numeroCaratteriDescrizione += 0.67

        numeroRighe = int(numeroCaratteriDescrizione/ caratteriPerRiga)
        resto = numeroCaratteriDescrizione % caratteriPerRiga

        if numeroRighe <= 1:
            lunghezzaRigaCm = 0.9

        else:
            addedCm = 0
            for i in range(1, numeroRighe):
                addedCm += 0.4

            lunghezzaRigaCm = 0.9 + addedCm

        if numeroRighe >= 1 and resto > 0:
            lunghezzaRigaCm += 0.4


        return lunghezzaRigaCm


    def __calcolaLavorazioniSuMisuraPerPaginaPreventivo__(lavorazioni, sconto, budget):

        grandezzaRighe = []

        caratteriPerRiga = 30

        lastSettore = ''

        # Per ogni lavorazione calcolo l'altezza della corrispondente riga nel preventivo
        for lav in lavorazioni:
            actualIndex = 0
            for sottolav in lav[3]:

                lunghezzaRigaCm = PdfGenerator.__calcolaGrandezzaRigaInCm__(sottolav.nome_modificato, caratteriPerRiga)


                # se la riga e' la prima di un nuovo settore di lavorazione allora al calcolo della
                # sua grandezza sommo la riga del titolo del settore
                if lav[0].copia:
                    if lastSettore != lav[0].settore_lav_copia:
                        lastSettore = lav[0].settore_lav_copia
                        lunghezzaRigaCm += 0.9
                else:
                    if lastSettore != lav[0].settore:
                        lastSettore = lav[0].settore
                        lunghezzaRigaCm += 0.9

                #l'ultima sottolavorazione a l'assistenza vengono sempre accoppiati e quindi la
                #dimensione viene calcolata come quella di un'unica riga
                if actualIndex == len(lav[3])-1:
                    if lav[0].assistenza != 'No assistenza':
                        lunghezzaRigaCm +=  PdfGenerator.__calcolaGrandezzaRigaInCm__(lav[0].assistenza, caratteriPerRiga)

                    #se budget aggiungo le dimensioni delle righe fornitura e posa
                    if budget:
                        lunghezzaRigaCm += 0.9+0.4#*2

                grandezzaRighe.append(round(lunghezzaRigaCm * 100) / 100)

        if len(grandezzaRighe) > 0:
            indexesToRet = []
            numPag = 1

            index, continua = PdfGenerator.__calcoraIndiceLastLavorazionePrimaPagina__(grandezzaRighe, sconto)

            indexesToRet.append(index)

            while continua and index+1 < len(grandezzaRighe):

                index, continua = PdfGenerator.__calcolaIndiceLastLavorazionePagineIntermedie__(index, grandezzaRighe[index+1:len(grandezzaRighe)], sconto)

                indexesToRet.append(index)
                numPag += 1

            if continua:
                numPag += 1

            if len(indexesToRet) < numPag:
                indexesToRet.append( indexesToRet[-1])
                indexesToRet[-2] = indexesToRet[-2]-1

            totLunghezzaUltimaPag = 0

            if len(indexesToRet) > 1:

                for lunghezza in grandezzaRighe[indexesToRet[-2]:len(grandezzaRighe)]:
                    totLunghezzaUltimaPag += lunghezza

                totLunghezzaUltimaPag = round(totLunghezzaUltimaPag*100)/100

                if totLunghezzaUltimaPag <= 6:
                    return (indexesToRet, False)
                else:
                    return (indexesToRet, True)
            else:

                return (indexesToRet, True)

        else:
            return ([], False)

    def __calcolaLavorazioniACorpoPerPaginaPreventivo__(lavorazioni, sconto):
        '''

        I parametri acorpo e sconto sono dei booleani.

        Una lavorazione il cui nome occupa una sola riga è altra 0.9 cm ed ogni riga extra aggiunge un 0.4cm;
        Una lavorazione occupa una sola riga se il suo numero di caratteri <= 50 se il preventivo e' a corpo
        altrimenti <= 12.
        Per quanto riguarda la prima facciata, un insieme di lavorazioni sta tutto
        in una pagina se l'altezza dell'insieme di
        righe delle lavorazioni ( con il totale ) è <= 7.2cm; se la riga dello sconto non compare il limite di
        7.2cm si trasforma in 8.1cm. Se l'insieme di lavorazioni supera questo limite allora nella prima facciata
        l'insieme delle lavorazioni non potrà superare i 9.9cm.
        Nelle pagine successive alla prima, se il totale è presente con lo sconto, il numero di righe
        avrà come limite i 13.5cm, senza sconto 14.4cm
        mentre, se il totale va su un'altra pagina ancora, il limite sarà di 17.1cm.
        Se il totale finisce sull'ultima pagina assieme ad esso potremmo avere al massimo un numero di lavorazioni
        che non superi i 4.5cm;


        :return: ritorna una tupla di due elementi dove_
                -prima pos: una lista dove il numero di elementi indica il numero di pagine necessarie per
                            stampare il preventivo e ogni elemento indica il numero dell'ultima lavorazione
                            nella pagina;
                -seconda pos: un booleano indicante se nell'ultima pagina il numero di lavorazioni supera i 4.5cm

        '''

        grandezzaRighe = []


        caratteriPerRiga = 50

        lastSettore = ''

        # Per ogni lavorazione calcolo l'altezza della corrispondente riga nel preventivo
        for lav in lavorazioni:

            lunghezzaRigaCm = PdfGenerator.__calcolaGrandezzaRigaInCm__(lav[0].nome_modificato, caratteriPerRiga)


            # se la riga e' la prima di un nuovo settore di lavorazione allora al calcolo della
            # sua grandezza sommo la riga del titolo del settore
            if lav[0].copia:
                if lastSettore != lav[0].settore_lav_copia:
                    lastSettore = lav[0].settore_lav_copia
                    lunghezzaRigaCm += 0.9
            else:
                if lastSettore != lav[0].settore:
                    lastSettore = lav[0].settore
                    lunghezzaRigaCm += 0.9

            #assieme alla riga della lavorazione considero anche quella dell'assistenza associata

            if  lav[0].assistenza != 'No assistenza':
                lunghezzaRigaCm +=  PdfGenerator.__calcolaGrandezzaRigaInCm__(lav[0].assistenza, caratteriPerRiga)

            grandezzaRighe.append(round(lunghezzaRigaCm * 100) / 100)


        if len(grandezzaRighe) > 0:
            indexesToRet = []
            numPag = 1

            index, continua = PdfGenerator.__calcoraIndiceLastLavorazionePrimaPagina__(grandezzaRighe, sconto)

            indexesToRet.append(index)

            while continua and index+1 < len(grandezzaRighe):

                index, continua = PdfGenerator.__calcolaIndiceLastLavorazionePagineIntermedie__(index, grandezzaRighe[index+1:len(grandezzaRighe)], sconto)

                indexesToRet.append(index)
                numPag += 1

            if continua:
                numPag += 1

            if len(indexesToRet) < numPag:
                indexesToRet.append( indexesToRet[-1])
                indexesToRet[-2] = indexesToRet[-2]-1


            totLunghezzaUltimaPag = 0

            if len(indexesToRet) > 1:

                for lunghezza in grandezzaRighe[indexesToRet[-2]:len(grandezzaRighe)]:
                   totLunghezzaUltimaPag += lunghezza

               # totLunghezzaUltimaPag = grandezzaRighe[len(grandezzaRighe)-1]
                totLunghezzaUltimaPag = round(totLunghezzaUltimaPag*100)/100

                if totLunghezzaUltimaPag <= 6:
                    return (indexesToRet, False)
                else:
                    return (indexesToRet, True)
            else:
                 return (indexesToRet, True)

        else:
            return ([], False)

    def __conclusionePreventivoLavorazioni__(budget, lastPageAlone):

        latexScript = ''

        if not budget:

            if lastPageAlone:
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
        return latexScript

    def __generaFilePdfPrevEdile__(latexScript, budget, sumisura, numero_preventivo, revisione ):

        nomeFileTex = ''

        if budget:
            nomeFileTex = 'budgetEdile-{}_{}.tex'.format(numero_preventivo, revisione)
        elif sumisura:
            nomeFileTex = 'preventivoEdile_suMisura-{}_{}.tex'.format(numero_preventivo, revisione)
        else:
            nomeFileTex = 'preventivoEdile-{}_{}.tex'.format(numero_preventivo, revisione)

        with open('app/preventiviLatexDir/{}'.format(nomeFileTex),
                  mode='w') as fileTex:
            fileTex.write(latexScript)

        os.system("cd app/preventiviLatexDir && pdflatex {}".format(nomeFileTex))

        # if chiudiPreventivo:
        #    os.system("cd app/preventiviLatexDir && rm *.tex *.aux *.log")

    def generaPdfPreventivoLavorazioni(edile, preventivo, codicePrev, commessa, dipendente, cliente, infoPreventivo,
                                            iva, tipoSconto, sconto, sumisura, budget):
        '''
            Questa funzione genera  sia il pdf del preventivo edile che quello del preventivo varianti,
            essendo questi identici tranne per un paio di diciture statiche.
            Si setta la funzione su un tipo di preventivo o l'altro attraverso il parametro booleano "edile".

            edile == true, preventivo edile
            edile == false, preventivo varianti
        '''


        latexScript = ''
        totaleToRet = 0

        if edile:
            latexScript += PdfGenerator.__generaIntestazionePreventivoEdile__(budget=budget, preventivo=preventivo, codicePrev=codicePrev,
                                                                commessa=commessa, dipendente=dipendente, cliente=cliente)


        headerLavorazioni =  PdfGenerator.__generaHederTabellaLavorazioni__( sumisura=sumisura, budget=budget )

       # latexScript += headerLavorazioni

        scontoRichiesto = True
        if tipoSconto == 1 or budget:
            scontoRichiesto = False

        numPagine = []
        lastPageAlone = False

        if sumisura or budget:
            numPagine, lastPageAlone = PdfGenerator.__calcolaLavorazioniSuMisuraPerPaginaPreventivo__(infoPreventivo[1],
                                                                                                        scontoRichiesto, budget)
        else:
            numPagine, lastPageAlone = PdfGenerator.__calcolaLavorazioniACorpoPerPaginaPreventivo__(infoPreventivo[1],
                                                                                                 scontoRichiesto)


        if sumisura or budget:
            latexScript += PdfGenerator.__costruisciCorpoPreventivoSuMisura__(infoPrev=infoPreventivo[1], numPagine=numPagine,
                                                                              lastPageAlone=lastPageAlone,
                                                                              headerLavorazioni= headerLavorazioni,
                                                                              budget=budget,
                                                                              tipoSconto=tipoSconto, sconto=sconto,
                                                                              iva=iva, preventivo=preventivo)

        else:
            scriptToAppend, totaleToRet= PdfGenerator.__costruisciCorpoPreventivoACorpo__(infoPreventivo[1], numPagine,
                                                                               lastPageAlone, headerLavorazioni,
                                                                               tipoSconto, sconto, iva)

            latexScript += scriptToAppend

        latexScript += PdfGenerator.__conclusionePreventivoLavorazioni__(budget, lastPageAlone)

        PdfGenerator.__generaFilePdfPrevEdile__(latexScript=latexScript, budget=budget, sumisura=sumisura,
                                                    numero_preventivo=preventivo.numero_preventivo, revisione=preventivo.revisione )

        return totaleToRet