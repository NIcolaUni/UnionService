from flask import render_template, redirect, request, url_for, session, request
from app import server, database, socketio, databaseManager
from app.model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room


####################################### ROUTE HANDLER #################################################



@server.route('/homeheader')
@login_required
def homeheader():
    return render_template('header_homepage.html')

@server.route('/gestioneDip', methods=['GET','POST'])
@login_required
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():
        databaseManager.registra( 'dipendenteFittizio', colonne=dict(username=form.username.data, password=form.password.data,
                                                classe=form.tipo_dip.data, dirigente=form.dirigente.data, creatoreCredenziali=current_user.get_id()))

        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
@login_required
def paginaProfilo():
    return render_template('paginaProfilo.html')


@server.route('/homepage')
@login_required
def homepage():
   # print("\n\n\n\nCiao io sono {0} con l'id {1}:\n\n\n".format(dip.username, dip.session_id))
   # emit('my response', {'data': 'brao semo!'})
    return render_template('homepage.html', dipendente=databaseManager.managerDipendente.dip)

@server.route('/sidebarLeft')
@login_required
def sidebarLeft():
    return render_template('sidebar-left.html', dipendente=databaseManager.managerDipendente.dip)

@server.route('/header')
@login_required
def header():
    return render_template('header.html', dipendente=databaseManager.managerDipendente.dip)

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        managerDipFittizio = databaseManager.managerDipendenteFittizio
        managerDipFittizio.setCurrentUser(username=current_user.get_id())

        res = databaseManager.search('dipendenteRegistrato',
                               colonneDesiderate=dict(password=True), parametriSearch=dict(password=form.password.data))
        if len(res) > 0:
            return render_template("registrazioneDip.html", form=form, fittizio=True, errPasswd=True)

        domicilioDip = form.resEDomUguali.data

        if domicilioDip:
            domicilioDip = form.residenza.data
        else:
            domicilioDip = form.domicilio.data

        username=databaseManager.registra('dipendente', currentFittizio=managerDipFittizio.dip,
                                     colonne=dict( nome=form.nome.data, cognome=form.cognome.data, cf=form.cf.data,
                                        dataNascita=form.dataNascita.data,
                                        residenza=form.residenza.data, domicilio=domicilioDip, telefono=form.telefono.data,
                                        password=form.password.dip,
                                        email_aziendale=form.email_aziendale.data, email_personale=form.email_personale.data,
                                        iban=form.iban.data, partitaIva=form.partitaIva.data, session_id=None ) )



        return render_template("confermaRegistrazione.html", username=username, password=form.password.data,
                                            creatoreCredenziali=managerDipFittizio.dip.creatoreCredenziali)

    return render_template("registrazioneDip.html", form=form, fittizio=True)


@server.route('/', methods=['GET','POST'])
@server.route('/login', methods=['GET','POST'])
def login():

    if current_user.is_authenticated:

        if databaseManager.managerDipendenteRegistrato.dip.fittizio:
            return redirect(url_for('registraDipendente'))
        return redirect(url_for('homepage'))

    form = LoginForm()


    if form.validate_on_submit():
        databaseManager.managerDipendenteRegistrato.setCurrentUser(username=form.username.data, password=form.password.data)

        if databaseManager.managerDipendenteRegistrato.dip is None:
            return render_template("login.html", form=form, error="Credenziali errate!")


        login_user(databaseManager.managerDipendenteRegistrato.dip, remember=True)


        return redirect(url_for('login'))

    return render_template("login.html", form=form)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


################################## SOCKETIO HANDLER ##########################################################

@socketio.on('my_event', namespace="/test")
def handle_my_event(message):
    server.logger.info('messagggio ricevuto: {}'.format(message['data']))
    #print('received message: ' + message)
    emit('my response', {'data': 'brao semo!'})

@socketio.on('registra_sid', namespace="/home")
def handle_registra_sid(message):
    server.logger.info('Registrazione sid dipendete: {0}, con sid {1}'.format(message['username'], request.sid))
    databaseManager.managerDipendente.updateSid(username=message['username'], sid=request.sid )


@socketio.on('registrazione_effettuata', namespace="/notifica")
def handle_registrazione_effetuata(message):

    responsabile = databaseManager.search('dipendente',
                               colonneDesiderate=dict(username=True), parametriSearch=dict(username=message['responsabile']))[0]
    nuovoDip = databaseManager.search('dipendente',
                               colonneDesiderate=dict(username=True), parametriSearch=dict(username=message['dipendente_registrato']))[0]


    databaseManager.managerNotifica.registraNotifica(dict(dipendente=responsabile.username,
                                                           titolo="Aggiunto nuovo dipendente",
                                                           contenuto="Il dipendente {0} {1} ha complatato la sua registrazione.".format(nuovoDip.nome, nuovoDip.cognome)
                                                               +"\nRicorda di completare i campi a te riservati"))


    emit('notificaRegistrazione', {'dipendente': message['dipendente_registrato']}, namespace='/notifica', room=responsabile.session_id)


@socketio.on_error('/home')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))