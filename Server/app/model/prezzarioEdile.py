from .db.prezzarioEdileDBmodel import PrezzarioEdileDBmodel

class PrezzarioEdile(PrezzarioEdileDBmodel):

    def __init__(self, settore, tipologia_lavorazione, pertinenza, costo=None, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None, daVerificare=False):
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
        self.costo = costo
        self.daVerificare = daVerificare

    def registraLavorazione(settore, tipologia_lavorazione, pertinenza, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None, costo=None):

        newLav = PrezzarioEdile(settore=settore, tipologia_lavorazione=tipologia_lavorazione, pertinenza=pertinenza,
                                    unitaMisura=unitaMisura, costo=costo, prezzoMin=prezzoMin, prezzoMax=prezzoMax,
                                    dimensione=dimensione, fornitura=fornitura, posa=posa, note=note)

        PrezzarioEdileDBmodel.commitLavorazione(newLav)

    def modificaLavorazione(settore, oldTipologia, tipologia_lavorazione, pertinenza, unitaMisura=None, prezzoMin=None, prezzoMax=None,
                        dimensione=None, fornitura=None, posa=None, note=None, costo=None):

        PrezzarioEdile.query.filter_by(settore=settore, tipologia_lavorazione=oldTipologia).update(

            {'settore': settore,
            'tipologia_lavorazione': tipologia_lavorazione,
            'pertinenza': pertinenza,
            'unitaMisura': unitaMisura,
            'costo': costo,
            'prezzoMin': prezzoMin,
            'prezzoMax': prezzoMax,
            'dimensione': dimensione,
            'fornitura': fornitura,
            'posa': posa,
            'note': note }
        );

        PrezzarioEdileDBmodel.commit()

    def eliminaLavorazione(settore, tipologia_lavorazione):

        toDel= PrezzarioEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).first()

        PrezzarioEdileDBmodel.commitEliminaLavorazione(toDel)

    def setDaVerificare(settore, tipologia_lavorazione, valore):
        PrezzarioEdile.query.filter_by(settore=settore, tipologia_lavorazione=tipologia_lavorazione).update({'daVerificare': valore})
        PrezzarioEdileDBmodel.commit()