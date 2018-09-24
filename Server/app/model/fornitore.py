from .db.fornitoreDBmodel import FornitoreDBmodel
from .settoreMerceologico import SettoreMerceologico
from .giorniPagamentoFornitore import GiorniPagamentoFornitore
from .modalitaPagamentoFornitore import ModalitaPagamentoFornitore
from .tipologiaPagamentoFornitore import TipologiaPagamentoFornitore
from .tempiDiConsegnaFornitore import TempiDiConsegnaFornitore
from sqlalchemy import exc, func
import app

class Fornitore(FornitoreDBmodel):

    def __init__(self,
                    primo_gruppo,
                    sotto_gruppo,
                    settoreMerceologico = None,
                    stato=None,
                    tempiDiConsegna = None,
                    prezziNetti = None,
                    scontoStandard = None,
                    scontoExtra1 = None,
                    scontoExtra2 = None,
                    trasporto = None,
                    imballo = None,
                    montaggio = None,
                    trasportoUnitaMisura=None,
                    imballoUnitaMisura = None,
                    montaggioUnitaMisura = None,
                    giorniPagamenti = None,
                    modalitaPagamenti = None,
                    tipologiaPagamenti = None,
                    provincia = None,
                    indirizzo = None,
                    telefono = None,
                    sito = None,
                    daVerificare = False):

        self.primo_gruppo=primo_gruppo
        self.sotto_gruppo=sotto_gruppo
        self.settoreMerceologico=settoreMerceologico
        self.stato=stato
        self.tempiDiConsegna=tempiDiConsegna
        self.prezziNetti=prezziNetti
        self.scontoStandard=scontoStandard
        self.scontoExtra1=scontoExtra1
        self.scontoExtra2=scontoExtra2
        self.trasporto=trasporto
        self.imballo = imballo
        self.montaggio = montaggio
        self.trasportoUnitaMisura=trasportoUnitaMisura
        self.imballoUnitaMisura=imballoUnitaMisura
        self.montaggioUnitaMisura=montaggioUnitaMisura
        self.giorniPagamenti=giorniPagamenti
        self.modalitaPagamenti=modalitaPagamenti
        self.tipologiaPagamenti=tipologiaPagamenti
        self.provincia=provincia
        self.indirizzo=indirizzo
        self.telefono=telefono
        self.sito=sito

    def registraFornitore(  primo_gruppo,
                            sotto_gruppo,
                            settoreMerceologico = None,
                            stato=None,
                            tempiDiConsegna = None,
                            prezziNetti = None,
                            scontoStandard = None,
                            scontoExtra1 = None,
                            scontoExtra2 = None,
                            trasporto=None,
                            imballo=None,
                            montaggio=None,
                            trasportoUnitaMisura=None,
                            imballoUnitaMisura=None,
                            montaggioUnitaMisura=None,
                            giorniPagamenti = None,
                            modalitaPagamenti = None,
                            tipologiaPagamenti = None,
                            provincia = None,
                            indirizzo = None,
                            telefono = None,
                            sito = None):

        aux = Fornitore.query.filter_by(primo_gruppo=primo_gruppo, sotto_gruppo=sotto_gruppo).first()

        if aux is not None:
            return (False, "Fornitore già registrato!")

        SettoreMerceologico.registraSettore(nome=settoreMerceologico)

        if tempiDiConsegna is not None:
            TempiDiConsegnaFornitore.registraTempiDiConsegna(nome=tempiDiConsegna)

        if giorniPagamenti is not None:
            GiorniPagamentoFornitore.registraGiorniPagamento(nome=giorniPagamenti)

        if modalitaPagamenti is not None:
            ModalitaPagamentoFornitore.registraModalitaPagamento(nome=modalitaPagamenti)

        if tipologiaPagamenti is not None:
            TipologiaPagamentoFornitore.registraTipologiaPagamento(nome=tipologiaPagamenti)

        if scontoStandard == '':
            scontoStandard=None

        if scontoExtra1 == '':
            scontoExtra1=None

        if scontoExtra2 == '':
            scontoExtra2=None

        if trasporto == '':
            trasporto=None

        if montaggio == '':
            montaggio=None

        if imballo == '':
            imballo=None


        newFornitore = Fornitore(primo_gruppo=primo_gruppo, sotto_gruppo=sotto_gruppo, settoreMerceologico=settoreMerceologico, stato=stato,
                                 tempiDiConsegna=tempiDiConsegna, prezziNetti=prezziNetti, scontoStandard=scontoStandard,
                                 scontoExtra1=scontoExtra1, scontoExtra2=scontoExtra2, trasporto=trasporto,
                                 trasportoUnitaMisura=trasportoUnitaMisura, montaggio=montaggio, montaggioUnitaMisura=montaggioUnitaMisura,
                                 imballo=imballo, imballoUnitaMisura=imballoUnitaMisura, giorniPagamenti=giorniPagamenti,
                                 modalitaPagamenti=modalitaPagamenti, tipologiaPagamenti=tipologiaPagamenti, provincia=provincia,
                                 indirizzo=indirizzo, telefono=telefono, sito=sito)



        FornitoreDBmodel.addRow(newFornitore)

        return (True, 'Fornitore registrato correttamente')


    def modificaFornitore(  primo_gruppo, sotto_gruppo, modifica):

        Fornitore.query.filter_by( primo_gruppo=primo_gruppo, sotto_gruppo=sotto_gruppo).update(modifica)

        FornitoreDBmodel.commit()


    def eliminaFornitore(primo_gruppo, sotto_gruppo):

        toDel = FornitoreDBmodel.query.filter_by(primo_gruppo=primo_gruppo, sotto_gruppo=sotto_gruppo).first()
        FornitoreDBmodel.delRow(toDel)