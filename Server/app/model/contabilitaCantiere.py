from .db.contabilitaCantiereDBmodel import ContabilitaCantiereDBmodel

class ContabilitaCantiere(ContabilitaCantiereDBmodel):

    def __init__(self, numero_preventivo, revisione, tipologia_lavorazione, budget,
                    costi_effettivi, fattura, ordine_lav):
        self.numero_preventivo = numero_preventivo
        self.revisione = revisione
        self.tipologia_lavorazione = tipologia_lavorazione
        self.budget = budget
        self.costi_effettivi = costi_effettivi
        self.fattura = fattura
        self.ordine_lav = ordine_lav

    def creaContabilita( numero_preventivo, revisione, tipologia_lavorazione, budget,
                    costi_effettivi, fattura, ordine_lav):

        newCont = ContabilitaCantiere( numero_preventivo=numero_preventivo, revisione=revisione,
                                       tipologia_lavorazione=tipologia_lavorazione, budget=budget,
                                       costi_effettivi=costi_effettivi, fattura=fattura,
                                       ordine_lav=ordine_lav)

        ContabilitaCantiere.addRow(newCont)

    def modificaContabilita(numero_preventivo, revisione, tipologia_lavorazione, modifica):

        ContabilitaCantiere.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                            tipologia_lavorazione=tipologia_lavorazione).update(modifica)

        ContabilitaCantiere.commit()