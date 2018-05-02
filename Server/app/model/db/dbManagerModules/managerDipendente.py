from app.model.dipendente import Dipendente
from app.model.dipendente import DipendenteRegistrato
from app.model.dirigente import Dirigente
from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean


class ManagerDipendente():

    def __init__(self, database, Dipentente):
        self.database = database
        self.dip = None


    def setCurrentUser(self, username):
        self.dip = Dipendente.query.filter_by(username=username).first()

    def updateSid(self, username, sid):
        Dipendente.query.filter_by(username=username).update({'session_id': sid})
        self.database.session.commit()

    def registraDipendente(self, colonne):

        username_candidato = "{0}_{1}".format(colonne['nome'], colonne['cognome']).lower()

        counter = 0
        if DipendenteRegistrato.query.filter_by(username=username_candidato).first() != None:
            counter = 1
            while DipendenteRegistrato.query.filter_by(username="{0}{1}".format(username_candidato, counter)).first() != None:
             counter += 1

        dip = None

        if counter == 0:
            dip = DipendenteRegistrato(username=username_candidato, password=colonne['password'], fittizio=False)
        else:
            dip = DipendenteRegistrato(username="{0}{1}".format(username_candidato, counter), password=colonne['password'], fittizio=False)



        newDip = Dipendente(nome=colonne['nome'], cognome=colonne['cognome'], cf=colonne['cf'],
                                dataNascita=colonne['dataNascita'],
                                residenza=colonne['residenza'], domicilio=colonne['domicilio'], telefono=colonne['telefono'],
                                username=dip.username, password=dip.password, email_aziendale=colonne['email_aziendale'],
                                email_personale=colonne['email_personale'], iban=colonne['iban'], partitaIva=colonne['partitaIva'],
                                classe=currentFittizio.classe, dirigente=currentFittizio.dirigente, session_id=None)


        self.database.session.delete(currentFittizio)
        self.database.session.delete(DipendenteRegistrato.query.filter_by(username=currentFittizio.username).first())
        self.database.session.add(dip)
        self.database.session.commit()
        self.database.session.add(newDip)
        self.database.session.commit()

        if currentFittizio.dirigente:
            newDirigente = Dirigente(username=dip.username)
            self.database.session.add(newDirigente)
            self.database.session.commit()

        return dip.username

    def searchDipendenti(self, colonneDesiderate, cf=None, nome=None, cognome=None,
                                username=None, password=None, dataNascita=None,
                                residenza=None, domicilio=None, telefono=None,
                                email_aziendale=None, email_personale=None,
                                iban=None, partitaIva=None, classe=None, dirigente=None):
        '''

        Ai parametri cf, nome, cognome, etc... vanno assegnati i valori servono per filtrare la query
        :param colonneDesiderate: da impostare usando DBManager.settaColonneDesiderateDipendente()
        :return: una lista di Dipententi
        '''


        firstCycle = True
        dipendenti = []  # lista di dipendenti selezionati da una query

        for key in colonneDesiderate.keys():
            if colonneDesiderate[key]:
                if key == 'cf':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(cf=cf)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.cf != cf:
                                dipendenti.remove(dip)

                elif key == 'nome':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(nome=nome)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.nome != nome:
                                dipendenti.remove(dip)

                elif key == 'cognome':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(cognome=cognome)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.cognome != cognome:
                                dipendenti.remove(dip)

                elif key == 'username':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(username=username)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.username != username:
                                dipendenti.remove(dip)

                elif key == 'password':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(password=password)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.password != password:
                                dipendenti.remove(dip)

                elif key == 'dataNascita':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(dataNascita=dataNascita)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.dataNascita != dataNascita:
                                dipendenti.remove(dip)

                elif key == 'residenza':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(residenza=residenza)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.residenza != residenza:
                                dipendenti.remove(dip)

                elif key == 'domicilio':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(domicilio=domicilio)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.domicilio != domicilio:
                                dipendenti.remove(dip)

                elif key == 'telefono':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(telefono=telefono)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.telefono != telefono:
                                dipendenti.remove(dip)

                elif key == 'email_aziendale':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(email_aziendale=email_aziendale)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.email_aziendale != email_aziendale:
                                dipendenti.remove(dip)

                elif key == 'email_personale':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(email_personale=email_personale)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.email_personale != email_personale:
                                dipendenti.remove(dip)

                elif key == 'iban':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(iban=iban)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.iban != iban:
                                dipendenti.remove(dip)

                elif key == 'partitaIva':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(partitaIva=partitaIva)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.partitaIva != partitaIva:
                                dipendenti.remove(dip)

                elif key == 'classe':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(classe=classe)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.classe != classe:
                                dipendenti.remove(dip)

                elif key == 'dirigente':
                    if firstCycle:
                        dipendenti = Dipendente.query.filter_by(dirigente=dirigente)
                        firstCycle = False
                    else:
                        for dip in dipendenti:
                            if dip.dirigente != dirigente:
                                dipendenti.remove(dip)

        return dipendenti



