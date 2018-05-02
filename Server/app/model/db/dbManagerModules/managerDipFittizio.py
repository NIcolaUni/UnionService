from app.model.dipendenteFittizio import DipendenteFittizio
from app.model.dipendenteRegistrato import DipendenteRegistrato

class ManagerDipendenteFittizio():

    def __init__(self, database):
        self.database = database
        self.dip = None


    def setCurrentUser(self, username):
        self.dip = DipendenteFittizio.query.filter_by(username=username).first()

    def registraDipendente(self, colonne):
        dipReg = DipendenteRegistrato(username=colonne['username'], password=colonne['password'], fittizio=True)
        newDipFittizio = DipendenteFittizio(username=colonne['username'], password=colonne['password'],
                                                classe=colonne['classe'], dirigente=colonne['dirigente'],
                                                    creatoreCredenziali=colonne['creatoreCredenziali'])
        self.database.session.add(dipReg)
        self.database.session.add(newDipFittizio)
        self.database.session.commit()


    def searchDipendenti(self, colonneDesiderate, username=None, password=None,
                            classe=None, dirigente=None, creatoreCredenziali=None ):
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
                        dipendenti = DipendenteFittizio.query.filter_by(username=username)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.username != username:
                                dipendenti.remove(dip)

                elif key == 'password':
                    if firstCycle:
                        dipendenti = DipendenteFittizio.query.filter_by(password=password)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.password != password:
                                dipendenti.remove(dip)

                elif key == 'classe':
                    if firstCycle:
                        dipendenti = DipendenteFittizio.query.filter_by(classe=classe)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.classe != classe:
                                dipendenti.remove(dip)

                elif key == 'dirigente':
                    if firstCycle:
                        dipendenti = DipendenteFittizio.query.filter_by(dirigente=dirigente)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.dirigente != dirigente:
                                dipendenti.remove(dip)


                elif key == 'creatoreCredenziali':
                    if firstCycle:
                        dipendenti = DipendenteFittizio.query.filter_by(creatoreCredenziali=creatoreCredenziali)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.creatoreCredenziali != creatoreCredenziali:
                                dipendenti.remove(dip)

        return dipendenti





