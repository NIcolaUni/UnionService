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
                    rincaroAzienda = None,
                    trasportoAzienda = None,
                    imballoAzienda = None,
                    trasportoAziendaUnitaMisura = None,
                    imballoAziendaUnitaMisura = None,
                    posa = None,
                    posaPerc = 50,
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


        self.rincaroAzienda = rincaroAzienda
        self.trasportoAzienda = trasportoAzienda
        self.imballoAzienda = imballoAzienda
        self.trasportoAziendaUnitaMisura = trasportoAziendaUnitaMisura
        self.imballoAziendaUnitaMisura = imballoAziendaUnitaMisura
        self.posa = posa
        self.posaPerc = posaPerc
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

                    rincaroAzienda=None,
                    trasportoAzienda=None,
                    imballoAzienda=None,
                    trasportoAziendaUnitaMisura=None,
                    imballoAziendaUnitaMisura=None,
                    posa = None,
                    posaPerc = 50,
                    nettoUsFornitura=None,

                    rincaroCliente=None,
                    versoDiLettura=None,
                    daVerificare=None):

        toTest = ModelloProdotto.query.filter_by(nome=nome, tipologia=tipologia, prodotto=prodotto, marchio=marchio).first()

        if toTest is None:

            newModello = ModelloProdotto(nome=nome, prodotto=prodotto, tipologia=tipologia, marchio=marchio, codice=codice,
                                           fornitore_primo_gruppo=fornitore_primo_gruppo, fornitore_sotto_gruppo=fornitore_sotto_gruppo,
                                            prezzoListinoFornitura=prezzoListinoFornitura,
                                            rincaroAzienda=rincaroAzienda, trasportoAzienda=trasportoAzienda, imballoAzienda=imballoAzienda,
                                            trasportoAziendaUnitaMisura=trasportoAziendaUnitaMisura,
                                            imballoAziendaUnitaMisura=imballoAziendaUnitaMisura,
                                            posa=posa, posaPerc=posaPerc,
                                            nettoUsFornitura=nettoUsFornitura,
                                            rincaroCliente=rincaroCliente, versoDiLettura=versoDiLettura,
                                            daVerificare=daVerificare)

            ModelloProdottoDBmodel.addRow(newModello)



    def eliminaModello(nome, prodotto, tipologia, marchio):

        toDel = ModelloProdotto.query.filter_by( nome=nome, prodotto=prodotto, tipologia=tipologia, marchio=marchio ).first()
        ModelloProdottoDBmodel.delRow(toDel)

    def modificaModello( modifica, nome, prodotto, tipologia, marchio ):

        toTest = ModelloProdotto.query.filter_by(nome=nome, prodotto=prodotto, tipologia=tipologia, marchio=marchio).first()

        if toTest is None:
            app.server.logger.info('\n\nWei sono nullo!! {} - {} - {} - {}\n\n'.format(nome, prodotto, tipologia, marchio))
        else:
            app.server.logger.info('\n\nWei non sono nullo!!\n\n')




        ModelloProdotto.query.filter_by(nome=nome, prodotto=prodotto, tipologia=tipologia, marchio=marchio).update( modifica )

        ModelloProdottoDBmodel.commit()

    def elimina(self):
        ModelloProdottoDBmodel.delRow(self)

    def setDaVerificare(modello, prodotto, marchio, tipologia, valore):

        app.server.logger.info('il modello {} prodotto {} marchio {} tipologia {} val {}\n\n\n'.format(modello, prodotto, marchio, tipologia, valore))

        ModelloProdottoDBmodel.query.filter_by(nome=modello, prodotto=prodotto, marchio=marchio, tipologia=tipologia).update({'daVerificare': valore})
        ModelloProdottoDBmodel.commit()

