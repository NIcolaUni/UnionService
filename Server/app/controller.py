from flask import render_template, redirect, request, url_for, session, request
from app import server, socketio, accoglienzaForm
from .model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm, ClienteAccoltoForm, ApriPaginaClienteForm
from .model.dipendenteFittizio import DipendenteFittizio
from .model.dipendenteRegistrato import DipendenteRegistrato
from .model.dipendente import Dipendente
from .model.notifica import Notifica
from .model.clienteAccolto import ClienteAccolto
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room
import app

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

@server.route('/apriPaginaCliente', methods=['POST'])
@login_required
def apriPaginaCliente():

    app.formCercaCliente = ApriPaginaClienteForm(request.form)
    scelta = app.formCercaCliente.nome_cognome_indirizzo.data
    (cognomeCliente, nomeCliente, indirizzoCliente) = scelta.split(" . ")
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    cliente = ClienteAccolto.query.filter_by(nome=nomeCliente, cognome=cognomeCliente, indirizzo=indirizzoCliente, commerciale=current_user.get_id()).first()

    return render_template('paginaCliente.html', dip=dip, cliente=cliente )


@server.route('/accoglienza/<int:error>', methods=['GET','POST'])
@login_required
def accoglienza(error):
    '''
    :param error:
    :return:
    '''

    '''
    Questo if è necessario poichè, al ritorno di una pagina per form non valido,
    la variabile accoglienzaForm viene sovrascritta con un form nuovo, ovvero quello
    richiamato dalla pagina stessa ritornata.
    '''
    if error == 1 :
        server.logger.info("\n\nEntrato in ERROR 1\n\n")
        if app.accoglienzaOk:
            app.accoglienzaOk=False
            return render_template('confermaRegistrazioneCliente.html')
        else:
            return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)

    app.accoglienzaForm = ClienteAccoltoForm(request.form)

    if request.method == 'POST':

        server.logger.info("\n\nEntrato in Post {}\n\n".format(app.accoglienzaForm))
        server.logger.info("\n\nEntrato in Post222 {}\n\n".format(app.accoglienzaForm.nome))

        if app.accoglienzaForm.validate_on_submit():
            server.logger.info("\n\n\nSono entrato nel validate!!!!\n\n\n")

            ClienteAccolto.registraCliente(nome=app.accoglienzaForm.nome.data, cognome=app.accoglienzaForm.cognome.data, indirizzo=app.app.accoglienzaForm.indirizzo.data,
                                           telefono=app.accoglienzaForm.telefono.data, email=app.accoglienzaForm.email.data, difficolta=app.accoglienzaForm.difficolta.data,
                                           tipologia=app.accoglienzaForm.tipologia.data, referenza=app.accoglienzaForm.referenza.data, sopraluogo=app.accoglienzaForm.sopraluogo.data,
                                           datasopraluogo=app.accoglienzaForm.datasopraluogo.data, lavorazione=app.accoglienzaForm.lavorazione.data, commerciale=current_user.get_id())

            app.accoglienzaOk=True
            return render_template('confermaRegistrazioneCliente.html')

    server.logger.info("\n\nAlternativa al post {}{}\n\n".format(app.accoglienzaForm.nome.errors, app.accoglienzaForm))

    return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)



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

    app.formCercaCliente = ApriPaginaClienteForm(request.form)

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    listaClienti = []

    if dip.classe == 'commerciale':
        listaClienti = ClienteAccolto.query.filter_by(commerciale=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()

    elif dip.classe == 'commerciale':
        listaClienti = ClienteAccolto.query.filter_by(tecnico=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()

    elif dip.classe == 'capocantiere':
        listaClienti = ClienteAccolto.query.filter_by(capocantiere=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()



    numNot = Notifica.get_counter(dipendente=current_user.get_id())
    return render_template('header.html', numNotifiche=numNot, listaClienti=listaClienti, form=app.formCercaCliente)

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        if Dipendente.query.filter_by(cf=form.cf.data).first() != None:
            return render_template("registrazioneDip.html", form=form, fittizio=True, errCf=True)

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