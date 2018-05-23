from .db.fornitoreDBmodel import FornitoreDBmodel
from app import Server

class Fornitore(FornitoreDBmodel):

    def __init__(self,
                    primo_gruppo,
                    sotto_gruppo = "",
                    settoreMerceologico = None,
                    tempiDiConsegna = None,
                    prezziNetti = None,
                    scontoStandard = None,
                    scontoExtra1 = None,
                    scontroExtra2 = None,
                    trasporto = None,
                    trasportoUnitaMisura = None,
                    giorniPagamenti = None,
                    modalitaPagamenti = None,
                    tipologiaPagamenti = None,
                    provincia = None,
                    indirizzo = None,
                    telefono = None,
                    sito = None):

        self.primo_gruppo=primo_gruppo
        self.sotto_gruppo=sotto_gruppo
        self.settoreMerceologico=settoreMerceologico
        self.tempiDiConsegna=tempiDiConsegna
        self.prezziNetti=prezziNetti
        self.scontoStandard=scontoStandard
        self.scontoExtra1=scontoExtra1
        self.scontroExtra2=scontroExtra2
        self.trasporto=trasporto
        self.trasportoUnitaMisura=trasportoUnitaMisura
        self.giorniPagamenti=giorniPagamenti
        self.modalitaPagamenti=modalitaPagamenti
        self.tipologiaPagamenti=tipologiaPagamenti
        self.provincia=provincia
        self.indirizzo=indirizzo
        self.telefono=telefono
        self.sito=sito

    def registraFornitore(  primo_gruppo,
                            sotto_gruppo = "",
                            settoreMerceologico = None,
                            tempiDiConsegna = None,
                            prezziNetti = None,
                            scontoStandard = None,
                            scontoExtra1 = None,
                            scontroExtra2 = None,
                            trasporto = None,
                            trasportoUnitaMisura = None,
                            giorniPagamenti = None,
                            modalitaPagamenti = None,
                            tipologiaPagamenti = None,
                            provincia = None,
                            indirizzo = None,
                            telefono = None,
                            sito = None):

        nuovoFornitore=Fornitore( primo_gruppo=primo_gruppo, sotto_gruppo=sotto_gruppo,settoreMerceologico=settoreMerceologico,
                                  tempiDiConsegna=tempiDiConsegna,
                                    prezziNetti=prezziNetti, scontoStandard=scontoStandard, scontoExtra1=scontoExtra1,
                                   scontroExtra2=scontroExtra2, trasporto=trasporto, trasportoUnitaMisura=trasportoUnitaMisura,
                                      giorniPagamenti=giorniPagamenti, modalitaPagamenti=modalitaPagamenti,
                                       tipologiaPagamenti=tipologiaPagamenti, provincia=provincia, indirizzo=indirizzo,
                                         telefono=telefono, sito=sito)

        FornitoreDBmodel.commitSettore(nuovoFornitore)
