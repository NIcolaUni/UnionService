from app.model.notifica import Notifica

class ManagerNotifica():

    def __init__(self, database):
        self.database = database
        self.listaNotifiche = []

    def setNotifiche(self, currentUser):
        self.listaNotifiche = Notifica.query.filter_by(username=currentUser)

    def registraNotifiche(self, colonne):
        daNotificare = Notifica(dipendente=colonne['dipendente'], titolo=colonne['titolo'],
                                contenuto=colonne['contenuto'])

        self.database.session.add(daNotificare)
        self.database.session.commit()

    def searchNotifica(self, colonneDesiderate, dipendente=None, titolo=None, contenuto=None):
        '''

        Ai parametri dipentente, titolo, etc... vanno assegnati i valori servono per filtrare la query
        :param colonneDesiderate: da impostare usando DBManager.settaColonneDesiderateNotifiche()
        :return: una lista di Notifiche
        '''

        firstCycle = True
        notifiche = []  # lista di notifiche selezionate da una query

        for key in colonneDesiderate.keys():
            if colonneDesiderate[key]:
                if key == 'dipendente':
                    if firstCycle:
                        notifiche = Notifica.query.filter_by(dipendente=dipendente)
                        firstCycle = False
                    else:
                        for nota in notifiche:
                            if nota.dipendente != dipendente:
                                notifiche.remove(nota)

                elif key == 'titolo':
                    if firstCycle:
                        notifiche = Notifica.query.filter_by(titolo=titolo)
                        firstCycle = False
                    else:
                        for nota in notifiche:
                            if nota.titolo != titolo:
                                notifiche.remove(nota)

                elif key == 'contenuto':
                    if firstCycle:
                        notifiche = Notifica.query.filter_by(contenuto=contenuto)
                        firstCycle = False
                    else:
                        for nota in notifiche:
                            if nota.contenuto != contenuto:
                                notifiche.remove(nota)

        return notifiche
