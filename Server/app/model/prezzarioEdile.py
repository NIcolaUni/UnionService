from .db.prezzarioEdileDBmodel import PrezzarioEdileDBmodel
from .lavorazioneEdile import LavorazioneEdile
import app

class PrezzarioEdile(PrezzarioEdileDBmodel):

    def __init__(self, ricaricoAzienda):
        self.ricaricoAzienda = ricaricoAzienda

    def registraPrezzario(ricaricoAzienda):

        oldPrez = PrezzarioEdile.query.first()

        #Può esistere solo un istanza della classe PrezzarioEdile
        if oldPrez is None:
            newPrez = PrezzarioEdileDBmodel(ricaricoAzienda=ricaricoAzienda)
            PrezzarioEdileDBmodel.addRow(newPrez)

    def modificaRicaricoPrezzario(newValueRincaro):

        PrezzarioEdile.registraPrezzario(50)

        PrezzarioEdileDBmodel.query.update({'ricaricoAzienda': newValueRincaro})
        PrezzarioEdileDBmodel.commit()

    def registraLavorazione(settore, tipologia_lavorazione, pertinenza, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None):

        PrezzarioEdile.registraPrezzario(50);
        LavorazioneEdile.registraLavorazione(settore=settore, tipologia_lavorazione=tipologia_lavorazione,
                                             pertinenza=pertinenza, unitaMisura=unitaMisura, prezzoMin=prezzoMin,
                                             prezzoMax=prezzoMax, dimensione=dimensione, fornitura=fornitura,
                                             posa=posa, note=note)

    def modificaLavorazione(settore, tipologia_lavorazione, modifica):

        LavorazioneEdile.modificaLavorazione(settore=settore, tipologia_lavorazione=tipologia_lavorazione, modifica=modifica)

    def modificaRicaricoLavorazione(settore, tipologia_lavorazione, valore):
        LavorazioneEdile.modificaRicaricoLavorazione(settore=settore, tipologia_lavorazione=tipologia_lavorazione, valore=valore)

    def eliminaLavorazione(settore, tipologia_lavorazione):

        LavorazioneEdile.eliminaLavorazione(settore=settore, tipologia_lavorazione=tipologia_lavorazione)

    def setDaVerificare(settore, tipologia_lavorazione, valore):

        LavorazioneEdile.setDaVerificare(settore=settore, tipologia_lavorazione=tipologia_lavorazione, valore=valore)

    def returnLavorazioni():

        return LavorazioneEdile.query.order_by(LavorazioneEdile.settore, LavorazioneEdile.tipologia_lavorazione)