from .db.dipendenteDBmodel import DipendenteDBmodel
from .db.dirigenteDBmodel import DirigenteDBmodel
from .dipendenteFittizio import DipendenteFittizio
from .dipendenteRegistrato import DipendenteRegistrato
from .dirigente import Dirigente
import os
import app

class Dipendente(DipendenteDBmodel):

    def __init__(self, cf, nome, cognome, username, password, dataNascita,
                 residenzaVia, residenzaNum, residenzaCitta, residenzaCap, residenzaRegione,
                 domicilioVia, domicilioNum, domicilioCitta, domicilioCap, domicilioRegione,
                 telefono, email_aziendale, email_personale,
                 iban, partitaIva, classe, dirigente, session_id=None):
        self.cf = cf
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password
        self.dataNascita = dataNascita
        self.residenzaVia = residenzaVia
        self.residenzaNum = residenzaNum
        self.residenzaCitta= residenzaCitta
        self.residenzaCap = residenzaCap
        self.residenzaRegione = residenzaRegione
        self.domicilioVia = domicilioVia
        self.domicilioNum = domicilioNum
        self.domicilioCitta = domicilioCitta
        self.domicilioCap = domicilioCap
        self.domicilioRegione = domicilioRegione
        self.telefono = telefono
        self.email_aziendale = email_aziendale
        self.email_personale = email_personale
        self.iban = iban
        self.partitaIva = partitaIva
        self.classe = classe
        self.dirigente = dirigente
        self.session_id = session_id

    # Equivalente al toString() di java
 #   def __repr__(self):
 #       return "<Dipendente - {0} {1}>".format(self.nome, self.cognome)

    def registraDipendente(dipFitUsername, nome, cognome, cf, dataNascita,
                           residenzaVia, residenzaNum, residenzaCitta, residenzaCap, residenzaRegione,
                           domicilioVia, domicilioNum, domicilioCitta, domicilioCap, domicilioRegione,
                           telefono,
                            password,
                            email_personale, iban, partitaIva):


        dipFittizio = DipendenteFittizio.query.filter_by(username=dipFitUsername).first();
        username_candidato = "{0}_{1}".format(nome, cognome).lower()

        counter = 0
        if DipendenteRegistrato.query.filter_by(username=username_candidato).first() != None:
            counter = 1
            while DipendenteRegistrato.query.filter_by(username="{0}{1}".format(username_candidato, counter)).first() != None:
                counter += 1

        dip = None

        if counter == 0:
            dip = DipendenteRegistrato(username=username_candidato, password=password, fittizio=False)
        else:
            dip = DipendenteRegistrato(username="{0}{1}".format(username_candidato, counter),
                                       password=password, fittizio=False)

        email_aziendale = '{}{}@servicegroup.biz'.format(nome, cognome)

        newDip = Dipendente(nome=nome, cognome=cognome, cf=cf,
                            dataNascita=dataNascita,
                            residenzaVia=residenzaVia, residenzaNum=residenzaNum, residenzaCitta=residenzaCitta,
                            residenzaCap=residenzaCap, residenzaRegione=residenzaRegione,
                            domicilioVia=domicilioVia, domicilioNum=domicilioNum, domicilioCitta=domicilioCitta,
                            domicilioCap=domicilioCap, domicilioRegione=domicilioRegione, telefono=telefono,
                            username=dip.username, password=dip.password, email_aziendale=email_aziendale,
                            email_personale=email_personale, iban=iban,
                            partitaIva=partitaIva,
                            classe=dipFittizio.classe, dirigente=dipFittizio.dirigente, session_id=None)

        isDirigente = dipFittizio.dirigente
        dirigenteResponsabile = dipFittizio.creatoreCredenziali

        DipendenteDBmodel.commitRegistrazione(DipendenteRegistrato.query.filter_by(username=dipFitUsername).first(), dip, newDip)


        if isDirigente:
            newDirigente = Dirigente(username=dip.username)
            DirigenteDBmodel.commitRegistrazione(newDirigente)

        return (dip.username, dip.password, dirigenteResponsabile)

    def registraSid(username, sid):
        Dipendente.query.filter_by(username=username).update({'session_id': sid})
        DipendenteDBmodel.commit()

    def salvaImmagineProfilo(username, file, dip):

        path_img = "{}.{}".format(dip.username, file.filename.split('.')[1] )


        if os.path.exists('./app/static/immaginiProfilo/{}'.format(path_img)):
            os.remove('./app/static/immaginiProfilo/{}'.format(path_img))
            path_img = "new_{}".format(path_img)


        elif os.path.exists('.app/static/immaginiProfilo/new_{}'.format(path_img)):
            os.remove('./app/static/immaginiProfilo/new_{}'.format(path_img))

        Dipendente.query.filter_by(username=username).update({'immagine_profilo': path_img})
        DipendenteDBmodel.commit()

        f = os.path.join(app.server.config['UPLOAD_FOLDER'], path_img)

        # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
        file.save(f)

    def modificaProfilo(username, modifica):

        Dipendente.query.filter_by(username=username).update(modifica)
        DipendenteDBmodel.commit()