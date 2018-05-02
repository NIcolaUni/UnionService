from app.model.dipendenteRegistrato import DipendenteRegistrato


class ManagerDipendenteRegistrato():

    def __init__(self, database):
        self.database = database
        self.dip = None


    def setCurrentUser(self, username, password=None):

        if password is not None:
            self.dip = DipendenteRegistrato.query.filter_by(username=username, password=password).first()
            return

        self.dip = DipendenteRegistrato.query.filter_by(username=username).first()

    def searchDipendenti(self, colonneDesiderate, username=None, password=None, fittizio=None):
        '''

        Ai parametri cf, nome, cognome, etc... vanno assegnati i valori servono per filtrare la query
        :param colonneDesiderate: da impostare usando DBManager.settaColonneDesiderateDipendente()
        :return: una lista di Dipententi
        '''

        firstCycle = True
        dipendenti = []  # lista di dipendenti selezionati da una query


        for key in colonneDesiderate.keys():
            if colonneDesiderate[key]:
                if key == 'username':
                    if firstCycle:
                        dipendenti = DipendenteRegistrato.query.filter_by(username=username)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.username != username:
                                dipendenti.remove(dip)

                elif key == 'password':
                    if firstCycle:
                        dipendenti = DipendenteRegistrato.query.filter_by(password=password)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.password != password:
                                dipendenti.remove(dip)

                elif key == 'fittizio':
                    if firstCycle:
                        dipendenti = DipendenteRegistrato.query.filter_by(fittizio=fittizio)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.fittizio != fittizio:
                                dipendenti.remove(dip)
        return dipendenti