from .db.sottoGruppoFornitoriDBmodel import SottoGruppoFornitoriDBmodel
from .eccezioni.righaPresenteException import RigaPresenteException
from sqlalchemy import exc, func
from .fornitore import Fornitore
import app

class SottoGruppoFornitori(SottoGruppoFornitoriDBmodel):

    def __init__(self,
                    nome,
                    gruppo_azienda,
                    settoreMerceologico = None,
                    stato=None,
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
                    sito = None,
                    daVerificare = False):

        self.nome=nome
        self.gruppo_azienda=gruppo_azienda
        self.settoreMerceologico=settoreMerceologico
        self.stato=stato
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
                            stato=None,
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

        if prezziNetti == 'True':
            prezziNetti=True
        else:
            prezziNetti=False

        nuovoFornitore=SottoGruppoFornitori( nome=nome, gruppo_azienda=gruppo_azienda,settoreMerceologico=settoreMerceologico,
                                     stato=stato, tempiDiConsegna=tempiDiConsegna,
                                    prezziNetti=prezziNetti, scontoStandard=scontoStandard, scontoExtra1=scontoExtra1,
                                   scontroExtra2=scontroExtra2, trasporto=trasporto, trasportoUnitaMisura=trasportoUnitaMisura,
                                      giorniPagamenti=giorniPagamenti, modalitaPagamenti=modalitaPagamenti,
                                       tipologiaPagamenti=tipologiaPagamenti, provincia=provincia, indirizzo=indirizzo,
                                         telefono=telefono, sito=sito)

        try:
            SottoGruppoFornitoriDBmodel.addRow(nuovoFornitore)
        except exc.SQLAlchemyError as e:
            SottoGruppoFornitoriDBmodel.rollback()
            app.server.logger.info('\n\n\n{}\n\n\n'.format(e))
            raise RigaPresenteException("Sottogruppo fornitore già presente")

    def eliminaSottoGruppoFornitori(nome, gruppo_azienda):

        app.server.logger.info("Sono quaaaa {} {}".format(nome, gruppo_azienda))
        toDel = SottoGruppoFornitori.query.filter_by(nome=nome, gruppo_azienda=gruppo_azienda).first()
        SottoGruppoFornitoriDBmodel.delRow(toDel)
        numSottoGruppi = SottoGruppoFornitori.countSottoGruppo(gruppo_azienda=gruppo_azienda)

        if numSottoGruppi == 0:
            Fornitore.setHas_sottoGruppi(gruppo_azienda, False)



    def countSottoGruppo(gruppo_azienda):
        q = SottoGruppoFornitori.query.filter_by(gruppo_azienda=gruppo_azienda)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count
