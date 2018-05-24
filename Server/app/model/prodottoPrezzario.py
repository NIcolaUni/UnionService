from .db.prodottoPrezzarioDBmodel import ProdottoPrezzarioDBmodel
from sqlalchemy import exc
from .eccezioni.righaPresenteException import RigaPresenteException
from app import server

class ProdottoPrezzario(ProdottoPrezzarioDBmodel):

    def __init__(self,
                    nome,
                    tipologia,
                    marchio = None,
                    codice = None,
                    fornitore_primo_gruppo = None,
                    fornitore_sotto_gruppo = None,
                    prezzoListino = None,
                    prezzoNettoListino = None,
                    rincaroNettoListino = None,
                    rincaroListino = None,
                    nettoUs = None,
                    rincaroTrasporto = None,
                    rincaroMontaggio = None,
                    scontoEx1 = None,
                    scontoEx2 = None,
                    scontoImballo = None,
                    rincaroTrasporto2 = None,
                    rincaroCliente = None ):

        self.nome=nome
        self.tipologia=tipologia
        self.marchio=marchio
        self.codice=codice
        self.fornitore_primo_gruppo=fornitore_primo_gruppo
        self.fornitore_sotto_gruppo=fornitore_sotto_gruppo
        self.prezzoListino=prezzoListino
        self.prezzoNettoListino=prezzoNettoListino
        self.rincaroNettoListino=rincaroNettoListino
        self.rincaroListino=rincaroListino
        self.nettoUs=nettoUs
        self.rincaroTrasporto=rincaroTrasporto
        self.rincaroMontaggio=rincaroMontaggio
        self.scontoEx1=scontoEx1
        self.scontoEx2=scontoEx2
        self.scontoImballo=scontoImballo
        self.rincaroTrasporto2=rincaroTrasporto2
        self.rincaroCliente =rincaroCliente


    def registraProdotto( nome,
                    tipologia,
                    marchio = None,
                    codice = None,
                    fornitore_primo_gruppo = None,
                    fornitore_sotto_gruppo = None,
                    prezzoListino = None,
                    prezzoNettoListino = None,
                    rincaroNettoListino = None,
                    rincaroListino = None,
                    nettoUs = None,
                    rincaroTrasporto = None,
                    rincaroMontaggio = None,
                    scontoEx1 = None,
                    scontoEx2 = None,
                    scontoImballo = None,
                    rincaroTrasporto2 = None,
                    rincaroCliente = None ):

        newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia, marchio=marchio, codice=codice,
                                         fornitore_primo_gruppo=fornitore_primo_gruppo, fornitore_sotto_gruppo=fornitore_sotto_gruppo,
                                         prezzoNettoListino=prezzoNettoListino, prezzoListino=prezzoListino, rincaroNettoListino=rincaroNettoListino,
                                          rincaroListino=rincaroListino, nettoUs=nettoUs, rincaroTrasporto=rincaroTrasporto,
                                          rincaroMontaggio=rincaroMontaggio, scontoEx1=scontoEx1, scontoEx2=scontoEx2,
                                          scontoImballo=scontoImballo, rincaroTrasporto2=rincaroTrasporto2, rincaroCliente=rincaroCliente)


        try:
            ProdottoPrezzarioDBmodel.commitProdotto(newProdotto)
        except exc.SQLAlchemyError as e:
            server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            ProdottoPrezzarioDBmodel.rollback()
            raise RigaPresenteException("Il prodotto inserito è già presente")