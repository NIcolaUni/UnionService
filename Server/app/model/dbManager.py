from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.model.db.dbManagerModules.managerDipendente import ManagerDipendente
from app.model.db.dbManagerModules.managerDipendenteFittizio import ManagerDipendenteFittizio
from app.model.db.dbManagerModules.managerDipendenteRegistrato import ManagerDipendenteRegistrato
from app.model.db.dbManagerModules.managerNotifica import ManagerNotifica

class DBManager():

    def __init__(self, server):

        self.database = SQLAlchemy(server)
        self.database.create_all()
        migrate = Migrate(server, self.database)

        manager = Manager(server)
        manager.add_command('db', MigrateCommand)


        self.managerDipendente = ManagerDipendente(self.database)
        self.managerDipendenteFittizio = ManagerDipendenteFittizio(self.database)
        self.managerDipendenteRegistrato = ManagerDipendenteRegistrato(self.database)
        self.managerNotifica = ManagerNotifica(self.database)

    def search(self, tabella, colonneDesiderate, parametriSearch):
        '''

        :param tabella: nome della tabella in cui fare la search
        :param colonneDesiderate: da impostare usando DBManager.settaColonneDesiderate__nometabella__()
        :param parametriSearch: dict avente key=nome_del parametro e value=valore_da_cercare
        :return: una lista di oggetti istanze di "tabella"
        '''
        if tabella == "dipendenteFittizio":
            aux= dict(username =None, password =None, classe =None, dirigente =None, creatoreCredenziali=None)

            for key in colonneDesiderate.keys():
                if colonneDesiderate[key]:
                    aux[key] = parametriSearch[key]

            return self.managerDipendenteFittizio.searchDipendenti(colonneDesiderate,
                                username =aux['username'], password =aux['password'], classe =aux['classe'],
                                    dirigente =aux['dirigente'], creatoreCredenziali=aux['creatoreCredenziali'])

        elif tabella == "dipendenteRegistrato":
            aux= dict(username =None, password =None, fittizio=None)

            for key in colonneDesiderate.keys():
                if colonneDesiderate[key]:
                    aux[key] = parametriSearch[key]

            return self.managerDipendenteRegistrato.searchDipendenti(colonneDesiderate,
                                username =aux['username'], password =aux['password'], fittizio=aux['fittizio'])

        elif tabella == "dipendente":

            aux= dict(cf =None, nome =None, cognome =None, username =None, password =None, dataNascita =None,
                                residenza =None, domicilio =None, telefono =None,
                                email_aziendale =None, email_personale =None,
                                iban=None, partitaIva =None, classe =None, dirigente =None)

            for key in colonneDesiderate.keys():
                if colonneDesiderate[key]:
                    aux[key] = parametriSearch[key]

            return self.managerDipendente.searchDipendenti(colonneDesiderate, cf=aux['cf'], nome=aux['nome'], cognome=aux['cognome'],
                                         username=aux['username'], password=aux['password'], dataNascita=aux['dataNascita'],
                                         residenza=aux['residenza'], domicilio=aux['domicilio'], telefono=aux['telefono'],
                                         email_aziendale=aux['email_aziendale'], email_personale=aux['email_personale'],
                                         iban=aux['iban'], partitaIva=aux['partitaIva'], classe=aux['classe'], dirigente=aux['dirigente'])

    def settaColonneDesiderateDipendente(self, cf=False, nome=False, cognome=False,
                                         username=False, password=False, dataNascita=False,
                                         residenza=False, domicilio=False, telefono=False,
                                         email_aziendale=False, email_personale=False,
                                         iban=False, partitaIva=False, classe=False, dirigente=False):
        '''
        Usato per selezionare i le colonne desiderate nel filtraggio di una query

        :param all: Se si vuole che vengano ritornate solo specifiche colonne il parametro all va
                        esplicitamente settato a false

        :return: un dict() dove key=nome_colonna e value=bool
        '''

        return { 'cf': cf, 'nome': nome, 'cognome': cognome, 'username': username, 'password': password,
                'dataNascita': dataNascita, 'residenza': residenza, 'domicilio': domicilio, 'telefono': telefono,
                'email_aziendale': email_aziendale, 'email_personale': email_personale, 'iban': iban,
                'partitaIva': partitaIva, 'classe': classe, 'dirigente': dirigente}


    def settaColonneDesiderateDipFittizio(self, username=False, password=False,
                                                 classe=False, dirigente=False, creatoreCredenziali=False):
        '''
        Usato per selezionare i le colonne desiderate nel filtraggio di una query

        :param all: Se si vuole che vengano ritornate solo specifiche colonne il parametro all va
                        esplicitamente settato a false

        :return: un dict() dove key=nome_colonna e value=bool
        '''

        return { 'username': username, 'password': password, 'classe': classe,
                    'dirigente': dirigente, 'creatoreCredenziali' : creatoreCredenziali}


    def settaColonneDesiderateDipRegistristrato(self, username=False, password=False,  fittizio=False):
        '''
        Usato per selezionare i le colonne desiderate nel filtraggio di una query

        :param all: Se si vuole che vengano ritornate solo specifiche colonne il parametro all va
                        esplicitamente settato a false

        :return: un dict() dove key=nome_colonna e value=bool
        '''

        return { 'username': username, 'password': password, 'fittizio': fittizio }

    def registra(self, tabella, colonne, currentFittizio=None):

        if tabella == "dipendente":
            return self.managerDipendente.registraDipendente(currentFittizio=currentFittizio, colonne=colonne)

        if tabella == "dipendenteFittizio":
            self.managerDipendenteFittizio.registraDipendente(colonne=colonne)
            return

