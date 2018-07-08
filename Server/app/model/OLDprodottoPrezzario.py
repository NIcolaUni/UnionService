from .db.prodottoPrezzarioDBmodel import ProdottoPrezzarioDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app
class ProdottoPrezzario(ProdottoPrezzarioDBmodel):

    def __init__(self,
                    nome,
                    tipologia,
                    marchio = None,
                    codice = None,
                    modello = None,
                    fornitore_primo_gruppo = None,
                    fornitore_sotto_gruppo = None,
                    prezzoListinoFornitura = None,
                    prezzoListinoFornituraPosa = None,
                    rincaroAzienda = None,
                    trasportoAzienda = None,
                    imballoAzienda = None,
                    trasportoAziendaUnitaMisura = None,
                    imballoAziendaUnitaMisura = None,
                    posa = None,
                    nettoUsFornituraPosa = None,
                    nettoUsFornitura = None,
                    rincaroCliente = None,
                    versoDiLettura = None,
                    daVerificare=None):

        self.nome=nome
        self.tipologia=tipologia
        self.marchio=marchio
        self.codice=codice
        self.modello=modello
        self.fornitore_primo_gruppo=fornitore_primo_gruppo
        self.fornitore_sotto_gruppo=fornitore_sotto_gruppo

        self.prezzoListinoFornitura = prezzoListinoFornitura
        self.prezzoListinoFornituraPosa = prezzoListinoFornituraPosa

        self.rincaroAzienda = rincaroAzienda
        self.trasportoAzienda = trasportoAzienda
        self.imballoAzienda = imballoAzienda
        self.trasportoAziendaUnitaMisura = trasportoAziendaUnitaMisura
        self.imballoAziendaUnitaMisura = imballoAziendaUnitaMisura
        self.posa = posa
        self.nettoUsFornituraPosa = nettoUsFornituraPosa
        self.nettoUsFornitura = nettoUsFornitura


        self.rincaroCliente =rincaroCliente
        self.versoDiLettura = versoDiLettura
        self.daVerificare = daVerificare


    def registraProdotto( nome,
                    tipologia,
                    marchio=None,
                    codice=None,
                    modello=None,
                    fornitore_primo_gruppo=None,
                    fornitore_sotto_gruppo=None,

                    prezzoListinoFornitura=None,
                    prezzoListinoFornituraPosa=None,

                    rincaroAzienda=None,
                    trasportoAzienda=None,
                    imballoAzienda=None,
                    trasportoAziendaUnitaMisura=None,
                    imballoAziendaUnitaMisura=None,
                    posa = None,
                    nettoUsFornituraPosa=None,
                    nettoUsFornitura=None,

                    rincaroCliente=None,
                    versoDiLettura=None,
                    daVerificare=None):

        newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia, marchio=marchio, codice=codice, modello=modello,
                                        fornitore_primo_gruppo=fornitore_primo_gruppo, fornitore_sotto_gruppo=fornitore_sotto_gruppo,
                                        prezzoListinoFornitura=prezzoListinoFornitura, prezzoListinoFornituraPosa=prezzoListinoFornituraPosa,
                                        rincaroAzienda=rincaroAzienda, trasportoAzienda=trasportoAzienda, imballoAzienda=imballoAzienda,
                                        trasportoAziendaUnitaMisura=trasportoAziendaUnitaMisura,
                                        imballoAziendaUnitaMisura=imballoAziendaUnitaMisura,
                                        posa=posa,
                                        nettoUsFornitura=nettoUsFornitura,
                                        nettoUsFornituraPosa=nettoUsFornituraPosa,
                                        rincaroCliente=rincaroCliente, versoDiLettura=versoDiLettura, daVerificare=daVerificare)


        try:
            ProdottoPrezzarioDBmodel.addRow(newProdotto)
        except exc.SQLAlchemyError as e:
            app.server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            ProdottoPrezzarioDBmodel.rollback()
            raise RigaPresenteException("Il prodotto inserito è già presente")


    def eliminaProdotto(nome, tipologia):

        toDel = ProdottoPrezzario.query.filter_by( nome=nome, tipologia=tipologia ).first()
        ProdottoPrezzarioDBmodel.delRow(toDel)

    def modificaProdotto( modifica ):

        oldNome =modifica.pop('oldNome')
        tipologia=modifica.pop('tipologia')

        ProdottoPrezzario.query.filter_by(nome=oldNome, tipologia=tipologia).update( modifica )

        ProdottoPrezzarioDBmodel.commit()

    def elimina(self):
        ProdottoPrezzarioDBmodel.delRow(self)

    def setDaVerificare(nome, tipologia, valore):
        app.server.logger.info("Entro qua {}".format(valore))
        ProdottoPrezzarioDBmodel.query.filter_by(nome=nome, tipologia=tipologia).update({'daVerificare': valore})
        ProdottoPrezzarioDBmodel.commit()

