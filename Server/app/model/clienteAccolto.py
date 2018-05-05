from .db.clienteAccoltoDBmodel import ClienteAccoltoDBmodel

class ClienteAccolto(ClienteAccoltoDBmodel):

    def __init__(self,
                 nome, cognome, indirizzo, telefono, email,
                  difficolta, tipologia, referenza, sopraluogo,
                    datasopraluogo, lavorazione, commerciale,
                        tecnico=None, capocantiere=None ):
        self.nome = nome
        self.cognome = cognome
        self. indirizzo = indirizzo
        self.telefono = telefono
        self. email = email
        self.difficolta = difficolta
        self.tipologia = tipologia
        self. referenza = referenza
        self.sopraluogo = sopraluogo
        self.datasopraluogo = datasopraluogo
        self.lavorazione = lavorazione
        self.commerciale = commerciale
        self.tecnico = tecnico
        self.capocantiere = capocantiere

    # Equivalente al toString() di java
    def __repr__(self):
        return "<Cliente Accolto - {0} {1}>".format(self.nome, self.cognome)

    def registraCliente(nome, cognome, indirizzo, telefono, email,
              difficolta, tipologia, referenza, sopraluogo,
                datasopraluogo, lavorazione, commerciale):

        cliente = ClienteAccolto(nome=nome, cognome=cognome, indirizzo=indirizzo, telefono=telefono,
                                 email=email, difficolta=difficolta, tipologia=tipologia, referenza=referenza,
                                 sopraluogo=sopraluogo,datasopraluogo=datasopraluogo, lavorazione=lavorazione,
                                 commerciale=commerciale)

        ClienteAccoltoDBmodel.commitClienteAccolto(cliente)

