from .db.lavorazioneEdileDBmodel import LavorazioneEdileDBmodel

class LavorazioneEdile(LavorazioneEdileDBmodel):

    def __init__(self, settore, tipologia_lavorazione, pertinenza, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None, ricaricoAzienda=50, daVerificare=False):
        self.settore = settore
        self.tipologia_lavorazione = tipologia_lavorazione
        self.pertinenza = pertinenza
        self.unitaMisura = unitaMisura
        self.prezzoMin = prezzoMin
        self.prezzoMax = prezzoMax
        self.dimensione = dimensione
        self.fornitura = fornitura
        self.posa = posa
        self.note = note
        self.ricaricoAzienda = ricaricoAzienda
        self.daVerificare = daVerificare

    def registraLavorazione(settore, tipologia_lavorazione, pertinenza, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None):

        if prezzoMax == '0':
            prezzoMax = int(posa)+int(fornitura)
        newLav = LavorazioneEdile(settore=settore, tipologia_lavorazione=tipologia_lavorazione, pertinenza=pertinenza,
                                    unitaMisura=unitaMisura,prezzoMin=prezzoMin, prezzoMax=prezzoMax,
                                    dimensione=dimensione, fornitura=fornitura, posa=posa, note=note)

        LavorazioneEdileDBmodel.addRow(newLav)

    def modificaLavorazione(settore, tipologia_lavorazione, modifica ):

        LavorazioneEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).update(modifica)

        LavorazioneEdileDBmodel.commit()

    def modificaRicaricoAll(valore):

        LavorazioneEdile.query.all().update({'ricaricoAzienda':valore})

    def modificaRicaricoLavorazione(settore, tipologia_lavorazione, valore):
        LavorazioneEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).update({'ricaricoAzienda': valore})

    def eliminaLavorazione(settore, tipologia_lavorazione):

        toDel= LavorazioneEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).first()

        LavorazioneEdileDBmodel.delRow(toDel)

    def setDaVerificare(settore, tipologia_lavorazione, valore):
        LavorazioneEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).update({'daVerificare': valore})
        LavorazioneEdileDBmodel.commit()