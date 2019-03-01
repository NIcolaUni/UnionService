from .db.contabilitaCantiereDBmodel import ContabilitaCantiereDBmodel
import app

class ContabilitaCantiere(ContabilitaCantiereDBmodel):

    def __init__(self, numero_preventivo, revisione, tipologia, budget,
                    costi_effettivi, fattura, ordine_lav, nome_lav ):
        self.numero_preventivo = numero_preventivo
        self.revisione = revisione
        self.tipologia = tipologia
        self.budget = budget
        self.costi_effettivi = costi_effettivi
        self.fattura = fattura
        self.ordine_lav = ordine_lav
        self.budget_imprevisti = 0
        self.costi_effettivi_budget_imprevisti = 0
        self.fattura_budget_imprevisti = 0
        self.nome_lav = nome_lav
        self.nome_artigiano = 'no artigiano'
        self.impego_artigiano = None

    def creaContabilita( numero_preventivo, revisione, tipologia , ordine_lav, budget,
                    costi_effettivi, fattura, nome_lav):

        newCont = ContabilitaCantiere( numero_preventivo=numero_preventivo, revisione=revisione,
                                       tipologia=tipologia, budget=budget,
                                       costi_effettivi=costi_effettivi, fattura=fattura,
                                       ordine_lav=ordine_lav, nome_lav=nome_lav)

        ContabilitaCantiere.addRow(newCont)

    def modificaContabilita(numero_preventivo, revisione, tipologia, ordine_lav, modifica):

        ContabilitaCantiere.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione,
                                            tipologia=tipologia, ordine_lav=ordine_lav).update(modifica)

        ContabilitaCantiere.commit()

    def modificaBudgetImprevistiContabilita(numero_preventivo, revisione, modifica):

        ContabilitaCantiere.query.filter_by(numero_preventivo=numero_preventivo, revisione=revisione).update(modifica)

        ContabilitaCantiere.commit()

    def impostaArtigiano(numero_preventivo, revisione, tipologia, ordine_lav, nome_artigiano, impiego_artigiano):

        ContabilitaCantiere.modificaContabilita(numero_preventivo=numero_preventivo, revisione=revisione,
                                                 tipologia=tipologia, ordine_lav=ordine_lav,
                                                 modifica={'nome_artigiano': nome_artigiano,
                                                           'impiego_artigiano': impiego_artigiano
                                                           })