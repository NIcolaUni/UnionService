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
                    rincaroListino = None,
                    nettoUs = None,
                    rincaroTrasporto = None,
                    rincaroMontaggio = None,
                    scontoUs = None,
                    scontoEx1 = None,
                    scontoEx2 = None,
                    scontoImballo = None,
                    rincaroTrasporto2 = None,
                    rincaroCliente = None,
                    daVerificare=None):

        self.nome=nome
        self.tipologia=tipologia
        self.marchio=marchio
        self.codice=codice
        self.fornitore_primo_gruppo=fornitore_primo_gruppo
        self.fornitore_sotto_gruppo=fornitore_sotto_gruppo
        self.prezzoListino=prezzoListino
        self.prezzoNettoListino=prezzoNettoListino
        self.rincaroListino=rincaroListino
        self.nettoUs=nettoUs
        self.rincaroTrasporto=rincaroTrasporto
        self.rincaroMontaggio=rincaroMontaggio
        self.scontoUs = scontoUs
        self.scontoEx1=scontoEx1
        self.scontoEx2=scontoEx2
        self.scontoImballo=scontoImballo
        self.rincaroTrasporto2=rincaroTrasporto2
        self.rincaroCliente =rincaroCliente
        self.daVerificare = daVerificare


    def registraProdotto( nome,
                    tipologia,
                    marchio = None,
                    codice = None,
                    fornitore_primo_gruppo = None,
                    fornitore_sotto_gruppo = None,
                    prezzoListino = None,
                    prezzoNettoListino = None,
                    rincaroListino = None,
                    nettoUs = None,
                    rincaroTrasporto = None,
                    rincaroMontaggio = None,
                    scontoUs = None,
                    scontoEx1 = None,
                    scontoEx2 = None,
                    scontoImballo = None,
                    rincaroTrasporto2 = None,
                    rincaroCliente = None,
                    daVerificare=None):

        newProdotto = ProdottoPrezzario(nome=nome, tipologia=tipologia, marchio=marchio, codice=codice,
                                         fornitore_primo_gruppo=fornitore_primo_gruppo, fornitore_sotto_gruppo=fornitore_sotto_gruppo,
                                         prezzoNettoListino=prezzoNettoListino, prezzoListino=prezzoListino,
                                          rincaroListino=rincaroListino, nettoUs=nettoUs, rincaroTrasporto=rincaroTrasporto,
                                          rincaroMontaggio=rincaroMontaggio, scontoUs=scontoUs, scontoEx1=scontoEx1, scontoEx2=scontoEx2,
                                          scontoImballo=scontoImballo, rincaroTrasporto2=rincaroTrasporto2, rincaroCliente=rincaroCliente,
                                          daVerificare=daVerificare)


        try:
            ProdottoPrezzarioDBmodel.commitProdotto(newProdotto)
        except exc.SQLAlchemyError as e:
            server.logger.info("\n\n\nci sono probelmi:\n {}\n\n\n".format(e))
            ProdottoPrezzarioDBmodel.rollback()
            raise RigaPresenteException("Il prodotto inserito è già presente")


    def eliminaProdotto(nome, tipologia):

        toDel = ProdottoPrezzario.query.filter_by( nome=nome, tipologia=tipologia ).first()
        ProdottoPrezzarioDBmodel.commitEliminaProdotto(toDel)

    def modificaProdotto( oldNome, nome,
                    tipologia,
                    marchio = None,
                    codice = None,
                    fornitore_primo_gruppo = None,
                    fornitore_sotto_gruppo = None,
                    prezzoListino = None,
                    prezzoNettoListino = None,
                    rincaroListino = None,
                    nettoUs = None,
                    rincaroTrasporto = None,
                    rincaroMontaggio = None,
                    scontoUs = None,
                    scontoEx1 = None,
                    scontoEx2 = None,
                    scontoImballo = None,
                    rincaroTrasporto2 = None,
                    rincaroCliente = None,
                    daVerificare = False ):

        ProdottoPrezzario.query.filter_by(nome=oldNome, tipologia=tipologia).update(

            {
                'nome': nome,
                'marchio': marchio,
                'codice': codice,
                'fornitore_primo_gruppo': fornitore_primo_gruppo,
                'fornitore_sotto_gruppo': fornitore_sotto_gruppo,
                'prezzoListino': prezzoListino,
                'prezzoNettoListino': prezzoNettoListino,
                'rincaroListino': rincaroListino,
                'nettoUs': nettoUs,
                'rincaroTrasporto': rincaroTrasporto,
                'rincaroMontaggio': rincaroMontaggio,
                'scontoUs': scontoUs,
                'scontoEx1': scontoEx1,
                'scontoEx2': scontoEx2,
                'scontoImballo': scontoImballo,
                'rincaroTrasporto2': rincaroTrasporto2,
                'rincaroCliente': rincaroCliente
             }
        );

        ProdottoPrezzarioDBmodel.commit()


    def setDaVerificare(tipo, prodotto, valore):
        ProdottoPrezzario.query.filter_by(tipologia=tipo, nome=prodotto).update({'daVerificare': valore})
        ProdottoPrezzarioDBmodel.commit()