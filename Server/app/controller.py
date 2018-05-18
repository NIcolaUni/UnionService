from flask import render_template, redirect, request, url_for, session, request
from app import server, socketio, accoglienzaForm
from .model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm, ClienteAccoltoForm, ApriPaginaClienteForm
from .model.dipendenteFittizio import DipendenteFittizio
from .model.dipendenteRegistrato import DipendenteRegistrato
from .model.dipendente import Dipendente
from .model.notifica import Notifica
from .model.settoreLavorazione import SettoreLavorazione
from .model.prezzarioEdile import PrezzarioEdile
from .model.clienteAccolto import ClienteAccolto
from .model.impegni import Impegni
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room
import app

####################################### ROUTE HANDLER #################################################

@server.route('/prezzarioEdile')
@login_required
def prezzarioEdile():
    #server.logger.info("\n\nchiamato {}\n\n".format(app.prezzarioEdileSettoreCorrente))
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    settori = SettoreLavorazione.query.all()
    #categorie = Categoria.query.all()
   # pertinenze = Pertinenza.query.all()
    lavorazioni = PrezzarioEdile.query.all()

    if app.prezzarioEdileSettoreCorrente is None:
        if len(lavorazioni) != 0:
            app.prezzarioEdileSettoreCorrente = lavorazioni[0].settore

    if app.prezzarioEdileSettoreCorrente is not None:

        #server.logger.info("\n\nchiamato {} {} {}\n\n".format(settori, categorie, pertinenze))
        return render_template('prezzario.html', dipendente=dip, settori=settori, settoreToSel=app.prezzarioEdileSettoreCorrente,
                                        lavorazioni=lavorazioni,
                                        sockUrl=app.appUrl, prezzario=True,)
    else:
        return render_template('prezzario.html', dipendente=dip, settori=settori, settoreToSel=None,
                                        lavorazioni=lavorazioni,
                                        sockUrl=app.appUrl, prezzario=True,)


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

'''
@server.route('/apriPaginaClienteAccoglienza/<nome>/<cognome>')
@login_required
def apriPaginaClienteAccoglienza(nome, cognome):
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    server.logger.info("\n\n\nStampa dipendente {}\n\n\n".format(dip))
    cliente = ClienteAccolto.query.filter_by(nome=nome, cognome=cognome, commerciale=current_user.get_id()).first()

    ufficioCommerciale = Dipendente.query.filter_by( classe="commerciale", username=cliente.commerciale )
    ufficioTecnico = Dipendente.query.filter_by( classe="tecnico", username=cliente.tecnico )
    ufficioCapicantiere = Dipendente.query.filter_by( classe="commerciale", username=cliente.capocantiere )
    settori = SettoreLavorazione.query.all()
    server.logger.info("\n\n\nStampa cliente {}\n\n\n".format(cliente))

    return render_template('paginaCliente.html', dip=dip, cliente=cliente, ufficioCommerciale=ufficioCommerciale,
                                    ufficioTecnico=ufficioTecnico, ufficioCapicantiere=ufficioCapicantiere, settori=settori )
'''



@server.route('/apriPaginaCliente', methods=['POST'])
@login_required
def apriPaginaCliente():

    app.formCercaCliente = ApriPaginaClienteForm(request.form)
    scelta = app.formCercaCliente.nome_cognome_indirizzo.data
    (cognomeCliente, nomeCliente, indirizzoCliente) = scelta.split(" . ")
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    cliente = ClienteAccolto.query.filter_by(nome=nomeCliente, cognome=cognomeCliente, indirizzo=indirizzoCliente, commerciale=current_user.get_id()).first()
    ufficioCommerciale = Dipendente.query.filter_by( classe="commerciale", username=cliente.commerciale )
    ufficioTecnico = Dipendente.query.filter_by( classe="tecnico", username=cliente.tecnico )
    ufficioCapicantiere = Dipendente.query.filter_by( classe="commerciale", username=cliente.capocantiere )
    settori = SettoreLavorazione.query.all()

    return render_template('paginaCliente.html', dip=dip, cliente=cliente, ufficioCommerciale=ufficioCommerciale,
                                    ufficioTecnico=ufficioTecnico, ufficioCapicantiere=ufficioCapicantiere, settori=settori )


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
    return render_template('homepage.html', dipendente=dip, sockUrl=app.appUrl)


@server.route('/impegni')
@login_required
def impegni():
    return render_template('impegni.html')

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


        return render_template("confermaRegistrazione.html", username=username, password=password, creatoreCredenziali=creatoreCredenziali, sockUrl=app.appUrl )

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

@server.route('/listImpegni')
@login_required
def listImpegni():

    impegni = Impegni.query.filter_by(dipendente=current_user.get_id())

    return render_template('impegni.html', impegni=impegni)

@server.route('/getImpegni')
@login_required
def getImpegni():

    returnList = '{"todo": "sono un impegno difficile", "dirigente": "gianni"},'
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


@socketio.on('registra_categoria', namespace='/prezzario')
def handle_registra_categoria(message):
    # verifico che il settore non sia gia presente

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    if Categoria.query.filter_by(nome=message['categoria']).first() is None:
        Categoria.registraCategoria(nome=message['categoria'])
        emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)
    else:
        emit('abortAggiorna', {'what': 'categoria'},namespace='/listino', room=dip.session_id)

@socketio.on('elimina_categoria', namespace="/prezzario")
def handle_elimina_settore(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    Categoria.eliminaCategoria(nome=message['categoria'])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('registra_pertinenza', namespace='/prezzario')
def handle_registra_pertinenza(message):
    # verifico che il settore non sia gia presente

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    if Pertinenza.query.filter_by(nome=message['pertinenza']).first() is None:
        Pertinenza.registraPertinenza(nome=message['pertinenza'])
        emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)
    else:
        emit('abortAggiorna', {'what': 'Pertinenza'},namespace='/listino', room=dip.session_id)

@socketio.on('elimina_pertinenza', namespace="/prezzario")
def handle_elimina_settore(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    Pertinenza.eliminaPertinenza(nome=message['pertinenza'])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('registra_settore', namespace="/prezzario")
def handle_registra_settore(message):

  #verifico che il settore non sia gia presente

  dip = Dipendente.query.filter_by(username=message['dip']).first()

  if SettoreLavorazione.query.filter_by(nome=message['settore'] ).first() is None:
      SettoreLavorazione.registraSettore(nome=message['settore'] )
      emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

  else:
      emit('abortAggiorna',  {'what': 'Settore'}, namespace='/prezzario', room=dip.session_id)


@socketio.on('elimina_settore', namespace="/prezzario")
def handle_elimina_settore(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    SettoreLavorazione.eliminaSettore(nome=message['settore'])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

@socketio.on('registra_lavorazione', namespace="/prezzario")
def handle_registra_lavorazione(message):
    server.logger.info("\n\n\nWei sono il dip: {}\n\n\n".format(message['dip']))
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    PrezzarioEdile.registraLavorazione(settore=message["settore"], tipologia_lavorazione=message["tipologia"],
                                        pertinenza=message["pertinenza"], unitaMisura=message["unita"],
                                         costo=message["costo"], prezzoMin=message["pMin"], prezzoMax=message["pMax"],
                                          dimensione=message["dimensione"], fornitura=message["fornitura"], posa=message["posa"],
                                            note=message["note"])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('cambia_settore_prezzario', namespace='/prezzario')
def handle_cambia_settore_prezzario(message):
    app.prezzarioEdileSettoreCorrente=message['settore']
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('setta_daVerificare', namespace='/prezzario')
def handle_setta_daVerificare(message):
    server.logger.info("\n\n\nMi è arrivato da registrare  {} {} {} \n\n\n".format(message['settore'], message['tipologia'], message['valore']))
    PrezzarioEdile.setDaVerificare(settore=message['settore'], tipologia_lavorazione=message['tipologia'], valore=message['valore'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

@socketio.on('elimina_lavorazione', namespace='/prezzario')
def handle_elimina_lavorazione(message):
    PrezzarioEdile.eliminaLavorazione(settore=message['settore'], tipologia_lavorazione=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('registraImpegno', namespace='/impegni')
def handle_registraImpegno(message):
    server.logger.info("Mi è arrivato da registrare per {}: {} ".format(message['dip'], message['testo']))

    if message['dir'] == "":
        Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'])
    else:
        Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'], dirigente=message['dir'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    emit('aggiornaImpegni', namespace='/impegni', room=dip.session_id)







@socketio.on_error('/impegni')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/home')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/notifica')
def error_handler_notifica(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/prezzario')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))
