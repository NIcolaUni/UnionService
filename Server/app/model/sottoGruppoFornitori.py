from .db.sottoGruppoFornitoriDBmodel import SottoGruppoFornitoriDBmodel
from .eccezioni.righaPresenteException import RigaPresenteException
from sqlalchemy import exc

class SottoGruppoFornitori(SottoGruppoFornitoriDBmodel):

    def __init__(self,
                    nome,
                    gruppo_azienda,
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

        self.nome=nome
        self.gruppo_azienda=gruppo_azienda
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

    def registraSottoGruppoFornitori(  nome,
                            gruppo_azienda = "",
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

        nuovoFornitore=SottoGruppoFornitori( nome=nome, gruppo_azienda=gruppo_azienda,settoreMerceologico=settoreMerceologico,
                                  tempiDiConsegna=tempiDiConsegna,
                                    prezziNetti=prezziNetti, scontoStandard=scontoStandard, scontoExtra1=scontoExtra1,
                                   scontroExtra2=scontroExtra2, trasporto=trasporto, trasportoUnitaMisura=trasportoUnitaMisura,
                                      giorniPagamenti=giorniPagamenti, modalitaPagamenti=modalitaPagamenti,
                                       tipologiaPagamenti=tipologiaPagamenti, provincia=provincia, indirizzo=indirizzo,
                                         telefono=telefono, sito=sito)

        try:
            SottoGruppoFornitoriDBmodel.commitSottoGruppo(nuovoFornitore)
        except exc.SQLAlchemyError as e:
            SottoGruppoFornitoriDBmodel.rollback()
            raise RigaPresenteException("Sottogruppo fornitore già presente")