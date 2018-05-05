from flask import render_template, redirect, request, url_for, session, request
from app import server, socketio
from .model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm
from .model.dipendenteFittizio import DipendenteFittizio
from .model.dipendenteRegistrato import DipendenteRegistrato
from .model.dipendente import Dipendente
from .model.notifica import Notifica
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room


####################################### ROUTE HANDLER #################################################

@server.route('/gestioneDip', methods=['GET','POST'])
@login_required
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():

        DipendenteFittizio.registraDipendente(username=form.username.data, password=form.password.data,
                                                classe=form.tipo_dip.data, dirigente=form.dirigente.data, creatoreCredenziali=current_user.get_id())

        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
@login_required
def paginaProfilo():
    return render_template('paginaProfilo.html')

@server.route('/accoglienza')
@login_required
def accoglienza():
    return render_template('accoglienzaCliente.html')

@server.route('/homepage')
@login_required
def homepage():

    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()

    return render_template('homepage.html', dipendente=dip)

@server.route('/sidebarLeft')
@login_required
def sidebarLeft():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('sidebar-left.html', dipendente=dip)

@server.route('/header')
@login_required
def header():

    numNot = Notifica.get_counter(dipendente=current_user.get_id())
    return render_template('header.html', numNotifiche=numNot)

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        '''
        cambiare controllo con cf
        if DipendenteRegistrato.query.filter_by(password=form.password.data).first() != None:
            return render_template("registrazioneDip.html", form=form, fittizio=True, errCf=True)
        '''
        domicilioDip = form.resEDomUguali.data

        if domicilioDip:
            domicilioDip = form.residenza.data
        else:
            domicilioDip = form.domicilio.data

        ( username, password, creatoreCredenziali ) = Dipendente.registraDipendente(dipFitUsername=current_user.get_id(), nome=form.nome.data, cognome=form.cognome.data,
                                cf=form.cf.data, dataNascita=form.dataNascita.data, residenza=form.residenza.data,
                                domicilio=domicilioDip, telefono=form.telefono.data,
                                password=form.password.data, email_aziendale=form.email_aziendale.data,
                                email_personale=form.email_personale.data, iban=form.iban.data, partitaIva=form.partitaIva.data )


        return render_template("confermaRegistrazione.html", username=username, password=password, creatoreCredenziali=creatoreCredenziali)

    return render_template("registrazioneDip.html", form=form, fittizio=True)


@server.route('/', methods=['GET','POST'])
@server.route('/login', methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        dip=DipendenteRegistrato.query.filter_by(username=current_user.get_id()).first()
        if dip.fittizio:
            return redirect(url_for('registraDipendente'))
        return redirect(url_for('homepage'))

    form = LoginForm()


    if form.validate_on_submit():
        dip=DipendenteRegistrato.query.filter_by(username=form.username.data, password=form.password.data).first()
        if dip is None:
            return render_template("login.html", form=form, error="Credenziali errate!")

        login_user(dip, remember=True)


        return redirect(url_for('login'))

    return render_template("login.html", form=form)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@server.route('/getNotifiche')
@login_required
def getNotifiche():
    notiche = Notifica.query.filter_by(dipendente=current_user.get_id());

    returnList = ""

    for nota in notiche:
        returnList += '{ "titolo": "' +nota.titolo+ '", "contenuto": "' + nota.contenuto +'" },'

    return '{ "list":[' +returnList[:-1]+'] }'

################################## SOCKETIO HANDLER ##########################################################

@socketio.on('my_event', namespace="/test")
def handle_my_event(message):
    server.logger.info('messagggio ricevuto: {}'.format(message['data']))
    #print('received message: ' + message)
    emit('my response', {'data': 'brao semo!'})

@socketio.on('registra_sid', namespace="/home")
def handle_registra_sid(message):
    Dipendente.registraSid(message['username'], request.sid)


@socketio.on('registrazione_effettuata', namespace="/notifica")
def handle_registrazione_effetuata(message):
    responsabile = Dipendente.query.filter_by(username=message['responsabile']).first()
    nuovoDip = Dipendente.query.filter_by(username=message['dipendente_registrato']).first()


    Notifica.registraNotifica(dipendente=responsabile.username, titolo="Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                              contenuto="Ricorda di completare la sua registrazione.")

    emit('aggiornaNotifiche', {'titolo': "Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                               'contenuto': "Ricorda di completare la sua registrazione."},
                                namespace='/notifica', room=responsabile.session_id)


@socketio.on_error('/home')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/notifica')
def error_handler_notifica(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))