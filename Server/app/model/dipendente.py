from app.model.db.dipendenteDBmodel import DipendenteDBmodel


class Dipendente(DipendenteDBmodel):

    def __init__(self, cf, nome, cognome, username, password, dataNascita,
                 residenza, domicilio, telefono, email_aziendale, email_personale,
                 iban, partitaIva, classe, dirigente, session_id):
        self.cf = cf
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.dataNascita = dataNascita
        self.residenza = residenza
        self.domicilio = domicilio
        self.telefono = telefono
        self.email_aziendale = email_aziendale
        self.email_personale = email_personale
        self.iban = iban
        self.partitaIva = partitaIva
        self.classe = classe
        self.dirigente = dirigente
        self.session_id = session_id

    # Equivalente al toString() di java
    def __repr__(self):
        return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)
