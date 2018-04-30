from app.model.db.notificaDBmodel import NotificaDBmodel


class Notifica(NotificaDBmodel):

    def __init__(self, dipendente, dirigente, titolo, contenuto):
        self.dipendente = dipendente
        self.dirigente = dirigente
        self.titolo = titolo
        self.contenuto = contenuto


    # Equivalente al toString() di java
    def __repr__(self):
        return "<Notifica: {0} per il dipendente {1} >".format(self.titolo, self.dipendente)
