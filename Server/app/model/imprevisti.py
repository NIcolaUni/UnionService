from .db.imprevistiDBmodel import ImprevistiDBmodel
import app


class Imprevisti(ImprevistiDBmodel):

    def __init__(self, nome, numero_preventivo, revisione, costo, costo_fattura, ordine, tipologia='edile',
                    nome_artigiano='no artigiano', impiego_artigiano=None):
        self.nome = nome
        self.numero_preventivo = numero_preventivo
        self.revisione = revisione
        self.tipologia = tipologia
        self.ordine = ordine
        self.costo = costo
        self.costo_fattura = costo_fattura
        self.nome_artigiano = nome_artigiano
        self.impiego_artigiano = impiego_artigiano


    def registraImprevisto( numero_preventivo, revisione, ordine):

        imp = ImprevistiDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                            revisione=revisione, ordine=ordine).first()

        if imp is None:
            newImp = Imprevisti(nome='', numero_preventivo=numero_preventivo, revisione=revisione,
                                        costo=0, costo_fattura=0, ordine=ordine)

            ImprevistiDBmodel.addRow(newImp)

    def eliminaImprevisto(numero_preventivo, revisione, ordine):
        toDel = ImprevistiDBmodel.query.filter_by( numero_preventivo=numero_preventivo,
                                                   revisione=revisione, ordine=ordine ).first()
        ImprevistiDBmodel.delRow(toDel)

    def modificaImprevisto( numero_preventivo, revisione, ordine, modifica):
        ImprevistiDBmodel.query.filter_by( numero_preventivo=numero_preventivo,
                                            revisione=revisione, ordine=ordine).update(modifica)

        ImprevistiDBmodel.commit()

    def impostaArtigiano( numero_preventivo, revisione, ordine, nome_artigiano, impiego_artigiano):
        app.server.logger.info('\n\n\nSn qua {} ::: {}\n\n'.format(nome_artigiano, ordine))
        ImprevistiDBmodel.query.filter_by(numero_preventivo=numero_preventivo,
                                          revisione=revisione, ordine=ordine).update({
                                                'nome_artigiano': nome_artigiano,
                                                'impiego_artigiano': impiego_artigiano
                                      })

        ImprevistiDBmodel.commit()
