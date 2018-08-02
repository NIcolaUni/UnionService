from .db.modelloProdottoDBmodel import ModelloProdottoDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
import app
class ModelloProdotto(ModelloProdottoDBmodel):

    def __init__(self,
                    nome,
                    prodotto,
                    tipologia,
                    marchio = None,
                    codice = None,
                    fornitore_primo_gruppo=None,
                    fornitore_sotto_gruppo=None,

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
        self.prodotto=prodotto
        self.tipologia=tipologia
        self.marchio=marchio
        self.codice=codice
        self.fornitore_primo_gruppo = fornitore_primo_gruppo
        self.fornitore_sotto_gruppo = fornitore_sotto_gruppo

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

    def registraModello( nome,
                    prodotto,
                    tipologia,
                    marchio=None,
                    codice=None,
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

        newModello = ModelloProdotto(nome=nome, prodotto=prodotto, tipologia=tipologia, marchio=marchio, codice=codice,
                                       fornitore_primo_gruppo=fornitore_primo_gruppo, fornitore_sotto_gruppo=fornitore_sotto_gruppo,
                                        prezzoListinoFornitura=prezzoListinoFornitura, prezzoListinoFornituraPosa=prezzoListinoFornituraPosa,
                                        rincaroAzienda=rincaroAzienda, trasportoAzienda=trasportoAzienda, imballoAzienda=imballoAzienda,
                                        trasportoAziendaUnitaMisura=trasportoAziendaUnitaMisura,
                                        imballoAziendaUnitaMisura=imballoAziendaUnitaMisura,
                                        posa=posa,
                                        nettoUsFornitura=nettoUsFornitura,
                                        nettoUsFornituraPosa=nettoUsFornituraPosa,
                                        rincaroCliente=rincaroCliente, versoDiLettura=versoDiLettura,
                                        daVerificare=daVerificare)


        try:
            ModelloProdottoDBmodel.addRow(newModello)
        except exc.SQLAlchemyError as e:
            app.server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            ModelloProdottoDBmodel.rollback()
            raise RigaPresenteException("Il prodotto inserito è già presente")


    def eliminaModello(nome, prodotto, tipologia):

        toDel = ModelloProdotto.query.filter_by( nome=nome, prodotto=prodotto, tipologia=tipologia ).first()
        ModelloProdottoDBmodel.delRow(toDel)

    def modificaModello( modifica, nome, prodotto, tipologia ):


        ModelloProdotto.query.filter_by(nome=nome, prodotto=prodotto, tipologia=tipologia).update( modifica )

        ModelloProdottoDBmodel.commit()

    def elimina(self):
        ModelloProdottoDBmodel.delRow(self)

    def setDaVerificare(modello, prodotto, marchio, tipologia, valore):

        app.server.logger.info('il modello {} prodotto {} marchio {} tipologia {}\n\n\n'.format(modello, prodotto, marchio, tipologia))

        ModelloProdottoDBmodel.query.filter_by(nome=modello, prodotto=prodotto, marchio=marchio, tipologia=tipologia).update({'daVerificare': valore})
        ModelloProdottoDBmodel.commit()

