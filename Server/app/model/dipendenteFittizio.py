from .db.dipFittizioDBmodel import DipFittizioDBmodel
from .dipendenteRegistrato import DipendenteRegistrato


class DipendenteFittizio(DipFittizioDBmodel):

    def __init__(self, username, password, classe, dirigente, creatoreCredenziali):
        self.username = username
        self.password = password
        self.classe = classe
        self.dirigente = dirigente
        self.creatoreCredenziali = creatoreCredenziali

    # Equivalente al toString() di java
    def __repr__(self):
        return "<DipendenteFittizio- {0}>".format(self.username)

    def registraDipendente( username, password, classe, dirigente, creatoreCredenziali):
        dipReg = DipendenteRegistrato(username=username, password=password, fittizio=True)
        newDipFittizio = DipendenteFittizio(username=username, password=password,
                                                classe=classe, dirigente=dirigente, creatoreCredenziali=creatoreCredenziali)

        DipFittizioDBmodel.commitRegistrazione(dipReg, newDipFittizio)

