from .db.personaleFornitoreDBmodel import PersonaleFornitoreDBmodel

class PersonaleFornitore(PersonaleFornitoreDBmodel):

    def __init__(self, nome, cognome, azienda_primo_gruppo, azienda_sotto_gruppo, telefono, email, ruolo):
        self.nome=nome
        self.cognome=cognome
        self.azienda_primo_gruppo=azienda_primo_gruppo
        self.azienda_sotto_gruppo=azienda_sotto_gruppo
        self.telefono=telefono
        self.email=email
        self.ruolo = ruolo


    def registraRappresentante(nome, cognome, azienda_primo_gruppo, azienda_sotto_gruppo, ruolo, telefono=None, email=None):

        oldRap =  PersonaleFornitore.query.filter_by(nome=nome, cognome=cognome,
                                                     azienda_primo_gruppo=azienda_primo_gruppo,
                                                     azienda_sotto_gruppo=azienda_sotto_gruppo ).first()

        if oldRap is not None:
            return (False, 'Personale già registrato')

        newRap = PersonaleFornitore(nome=nome, cognome=cognome, azienda_primo_gruppo=azienda_primo_gruppo, ruolo=ruolo,
                                    azienda_sotto_gruppo=azienda_sotto_gruppo, telefono=telefono, email=email)

        PersonaleFornitoreDBmodel.addRow(newRap)

        return (True, '')

    def modificaRappresentante(nome, cognome, azienda_primo_gruppo, azienda_sotto_gruppo, modifica):
        PersonaleFornitore.query.filter_by(nome=nome, cognome=cognome, azienda_primo_gruppo=azienda_primo_gruppo, azienda_sotto_gruppo=azienda_sotto_gruppo).update(modifica)

        PersonaleFornitoreDBmodel.commit()



    def eliminaRappresentante(nome, cognome, azienda_primo_gruppo, azienda_sotto_gruppo):
        toDel = PersonaleFornitore.query.filter_by(nome=nome, cognome=cognome, azienda_primo_gruppo=azienda_primo_gruppo, azienda_sotto_gruppo=azienda_sotto_gruppo).first()
        PersonaleFornitoreDBmodel.delRow(toDel)
