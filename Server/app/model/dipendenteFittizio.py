from app.model.db.dipFittizioDBmodel import DipFittizioDBmodel

class DipendenteFittizio(DipFittizioDBmodel):

    def __init__(self, username, password, classe, dirigente):
        self.username = username
        self.password = password
        self.classe = classe
        self.dirigente = dirigente

    # Equivalente al toString() di java
    def __repr__(self):
        return "<DipendenteFittizio- {0}>".format(self.username)
