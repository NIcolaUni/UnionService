from app.model.db.dipFittizioDBmodel import DipFittizioDBmodel

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
