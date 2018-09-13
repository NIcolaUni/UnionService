from .db.agendaDBmodel import AgendaDBmodel
import datetime
import app

class Agenda(AgendaDBmodel):

    def __init__(self, dipendente, titolo, giorno, inizio_ora,
                  fine_ora, accompagnatore_sopraluogo=None, cliente_sopraluogo=None, sopraluogo=False,
                 luogo_sopraluogo=None):

        self.dipendente = dipendente
        self.titolo = titolo
        self.giorno = giorno

        #self.tipologia = tipologia

        self.inizio_ora=inizio_ora
        self.fine_ora=fine_ora
        self.accompagnatore_sopraluogo=accompagnatore_sopraluogo
        self.cliente_sopraluogo=cliente_sopraluogo
        self.sopraluogo = sopraluogo
        self.luogo_sopraluogo=luogo_sopraluogo


    def registraAppuntamento( dipendente, titolo, giorno, inizio_ora, fine_ora,
                        accompagnatore_sopraluogo=None, cliente_sopraluogo=None, sopraluogo=False, luogo_sopraluogo=None):
        #ritorna true o false a seconda che l'appuntamento sia impostabile o meno

        inizioOra_toSet=datetime.datetime.strptime('{} {}'.format(giorno, inizio_ora), '%Y-%m-%d %H:%M')
        fineOra_toSet=datetime.datetime.strptime('{} {}'.format(giorno, fine_ora), '%Y-%m-%d %H:%M')



        appuntamenti = Agenda.query.filter_by(dipendente=dipendente, giorno=giorno).all()

        for appuntamento in appuntamenti:


            if appuntamento.inizio_ora >= inizioOra_toSet.time():

                #se i due appuntamenti non si accavallano  a appuntamento.inizio_ora si verifica piu' tardi
                if appuntamento.inizio_ora >= fineOra_toSet.time():

                    startH_noMicrosec=appuntamento.inizio_ora.__str__().split(':')[0]+':'+appuntamento.inizio_ora.__str__().split(':')[1]
                    dateTimeApp=datetime.datetime.strptime(appuntamento.giorno.__str__()+' '+startH_noMicrosec, '%Y-%m-%d %H:%M')

                    diff=dateTimeApp-fineOra_toSet

                    #prendo i minuti e li trasformo in intero
                    diff=int(diff.__str__().split(':')[1])

                    #se le due ora non distano almeno 15 min
                    if diff <= 15:
                        return False

                #se i due appuntamenti si accavallano
                else:
                    return False

            #se il nuovo appuntamento inizia dopo quello che si sta verificando
            else:

                # se i due appuntamenti si accavallano
                if appuntamento.fine_ora >= inizioOra_toSet.time():
                    return False

                #se il nuovo appuntamento si verifica poi
                else:
                    endH_noMicrosec = appuntamento.fine_ora.__str__().split(':')[0] + ':' + \
                                        appuntamento.fine_ora.__str__().split(':')[1]

                    dateTimeApp = datetime.datetime.strptime(
                        appuntamento.giorno.__str__() + ' ' + endH_noMicrosec, '%Y-%m-%d %H:%M')
                    diff=inizioOra_toSet-dateTimeApp

                    # prendo i minuti e li trasformo in intero
                    diff = int(diff.__str__().split(':')[1])

                    # se le due ora non distano almeno 15 min
                    if diff <= 15:
                        return False


        newAppuntamento = Agenda(dipendente=dipendente, titolo=titolo, giorno=giorno,
                           inizio_ora=inizio_ora, fine_ora=fine_ora,
                           accompagnatore_sopraluogo=accompagnatore_sopraluogo, cliente_sopraluogo=cliente_sopraluogo,
                           sopraluogo=sopraluogo, luogo_sopraluogo=luogo_sopraluogo)
        AgendaDBmodel.addRow(newAppuntamento)

        return True


    def eliminaAppuntamento( dipendente, giorno, inizio_ora ):

        toDel = AgendaDBmodel.query.filter_by(dipendente=dipendente, giorno=giorno, inizio_ora=inizio_ora).first()

        AgendaDBmodel.delRow(toDel)


    def cambiaOrarioInizioEvento(dipendente, giorno, old_inizio_ora, new_inizio_ora ):

        old_inizioOra_toSet = datetime.datetime.strptime('{} {}'.format(giorno, old_inizio_ora), '%Y-%m-%d %H:%M')
        new_inizioOra_toSet = datetime.datetime.strptime('{} {}'.format(giorno, new_inizio_ora), '%Y-%m-%d %H:%M')

        appuntamenti = Agenda.query.filter_by(dipendente=dipendente, giorno=giorno).all()



        #controllo che l'appuntamento non si sovrapponda ad altro distando almeni 15 min
        for appuntamento in appuntamenti:

            #se non e' l'appuntamento che vogliamo modificare
            if appuntamento.dipendente != dipendente and appuntamento.inizio_ora != old_inizioOra_toSet:

                if appuntamento.fine_ora <= new_inizioOra_toSet:
                    hour_noMicrosec = appuntamento.fine_ora.__str__().split(':')[0] + ':' + \
                                      appuntamento.fine_ora.__str__().split(':')[1]

                    dateTimeApp = datetime.datetime.strptime(
                        appuntamento.giorno.__str__() + ' ' + hour_noMicrosec, '%Y-%m-%d %H:%M')
                    diff = new_inizioOra_toSet - dateTimeApp

                    if diff <= 15:
                        return False

                else:
                    return False

        Agenda.query.filter_by(dipendente=dipendente, giorno=giorno, inizio_ora=old_inizio_ora).update({
            'inizio_ora': new_inizio_ora
        })

        AgendaDBmodel.commit()

        return True

    def cambiaOrarioFineEvento(dipendente, giorno, old_fine_ora, new_fine_ora):

        old_fineOra_toSet = datetime.datetime.strptime('{} {}'.format(giorno, old_fine_ora), '%Y-%m-%d %H:%M')
        new_fineOra_toSet = datetime.datetime.strptime('{} {}'.format(giorno, new_fine_ora), '%Y-%m-%d %H:%M')

        appuntamenti = Agenda.query.filter_by(dipendente=dipendente, giorno=giorno).all()

        # controllo che l'appuntamento non si sovrapponda ad altro distando almeni 15 min
        for appuntamento in appuntamenti:

            # se non e' l'appuntamento che vogliamo modificare
            if appuntamento.dipendente != dipendente and appuntamento.fine_ora != old_fineOra_toSet:

                if appuntamento.inizio_ora >= new_fineOra_toSet:
                    hour_noMicrosec = appuntamento.inizio_ora.__str__().split(':')[0] + ':' + \
                                      appuntamento.inizio_ora.__str__().split(':')[1]

                    dateTimeApp = datetime.datetime.strptime(
                        appuntamento.giorno.__str__() + ' ' + hour_noMicrosec, '%Y-%m-%d %H:%M')
                    diff =  dateTimeApp - new_fineOra_toSet

                    if diff <= 15:
                        return False

                else:
                    return False

        Agenda.query.filter_by(dipendente=dipendente, giorno=giorno, fine_ora=old_fine_ora).update({
            'fine_ora': new_fine_ora
        }).all()

        AgendaDBmodel.commit()

        return True